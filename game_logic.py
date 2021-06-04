import typing as tp
from time import mktime, strptime

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
        }
        self.game_logic = GameLogic()
        # self.players = tp.List[Player]
        # self.current_drawing = Player

    def send_draw(self, request: Request):
        return [request]

    def send_message(self, request: Request):
        data = request.data
        user = request.user

        print(self.clients.get_all_usernames())

        message = data['message']
        requests = list()

        result, points = self.game_logic.answer_result(message)
        if result:
            # Save them to user with username = user
            r = Request()
            r.headers['Action'] = 'UPDATE_CHAT'
            r.headers['Data'] = '{"message": "answer correct"}'
            requests.append(r)

            r2 = Request()
            r2.headers['Action'] = 'UPDATE_POINTS'
            r2.headers['Data'] = '{"message": [{"username": "malika", "points": 20}, {"username": "maciej", "points": 10}]}'
            requests.append(r2)

            print("Answer correct | [POINTS] -> ", points)
        else:
            r = Request()
            r.headers['Action'] = 'UPDATE_CHAT'
            r.headers['Data'] = '{"message": "' + f'{message}' + '"}'
            requests.append(r)

            print("Answer incorrect | [POINTS] -> ", points)

        return requests

    def dispatch(self, request: Request) -> tp.List[Request]:
        action = request.action
        function = self.dispatcher.get(action)
        if function is not None:
            return function(request)

        return []
