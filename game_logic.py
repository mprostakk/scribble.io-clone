import typing as tp
from time import mktime, strptime
import json

from utils import CustomClients
from words_list import words
from custom_request import Request


MAX_TIME = 120


class GameLogic:
    def __init__(self):
        self.current_word = 'apple'
        self.start_time = None

    def current_word_setter(self, value):
        self.current_word = value

    def start_time_setter(self, value):
        self.start_time = value.toEpoch()

    def count_points(self, answer_time):
        # pattern = '%H:%M:%S'
        # epoch = int(mktime(strptime(answer_time, pattern)))
        return 50

    def detect_answer(self, message):
        if self.current_word == message:
            return True
        for word in words[self.current_word]:
            if word == message:
                return True

        return False

    def answer_result(self, message):
        time = ''  # TODO - get time
        is_answer = self.detect_answer(message)
        if is_answer:
            points = self.count_points(time)
            return is_answer, points
        else:
            return is_answer, 0


class Game:
    def __init__(self, clients):
        self.clients: CustomClients = clients
        self.dispatcher = {
            'DRAW': self.send_draw,
            'SEND_MESSAGE': self.send_message,
            'INIT': self.get_new_user_requests
        }
        self.game_logic = GameLogic()
        self.started = False
        self.current_drawing = None
        self.points = dict()

    def start(self, request):
        if self.started is False:
            self.started = True
            self.current_drawing = self.clients.get_all_usernames()[0]

            requests = list()
            requests.append(self.get_current_word_request(request))
            requests.append(self.get_points_request())

            print(requests)

            return requests

        return []

    def send_draw(self, request: Request):
        if self.current_drawing == request.user:
            r = Request()
            r.headers['Action'] = 'DRAW'
            r.headers['Data'] = json.dumps(request.data)
            return [r]
        else:
            return []

    def get_new_user_requests(self, request):
        requests = list()
        s = self.start(request)
        requests.extend(s)

        requests.append(self.get_current_word_request(request))
        requests.append(self.get_points_request())
        return requests

    def get_current_word_request(self, request):
        r = Request()
        r.headers['Action'] = 'CURRENT_WORD'

        print(request.user, self.current_drawing)

        if request.user == self.current_drawing:
            data = {
                'message': self.game_logic.current_word
            }
        else:
            data = {
                'message': '***'
            }

        r.headers['Data'] = json.dumps(data)
        r.users_to_send.append(request.user)
        return r

    def get_points_request(self):
        r = Request()
        r.headers['Action'] = 'UPDATE_POINTS'
        player_points = list()
        for username in self.clients.get_all_usernames():
            points = self.points.get(username)
            if points is None:
                self.points[username] = 0
                points = 0

            player_points.append({
                'username': username,
                'points': points
            })

        data = {
            'message': player_points
        }

        r.headers['Data'] = json.dumps(data)
        return r

    def get_message_request(self, message):
        r = Request()
        r.headers['Action'] = 'UPDATE_CHAT'
        data = {
            'message': message
        }
        r.headers['Data'] = json.dumps(data)
        return r

    def send_message(self, request: Request):
        data = request.data
        user = request.user

        print(self.clients.get_all_usernames())

        message = data['message']
        requests = list()

        requests.append(self.get_current_word_request(request))

        result, points = self.game_logic.answer_result(message)
        if result:
            requests.append(self.get_message_request(f'{user}: Answer correct!'))
            self.points[user] += 10
            requests.append(self.get_points_request())
        else:
            requests.append(self.get_message_request(f'{user}: {message}'))

        return requests

    def dispatch(self, request: Request) -> tp.List[Request]:
        action = request.action
        function = self.dispatcher.get(action)
        if function is not None:
            return function(request)

        return []
