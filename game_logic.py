import typing as tp
from datetime import datetime
import json
from random import choice

from utils import CustomClients
from words_list import words
from custom_request import Request


MAX_TIME = 120


class GameLogic:
    def __init__(self):
        self.current_word = ''
        self.start_time = None

    def current_word_underlines(self):
        return '_ ' * len(self.current_word)

    def set_random_current_word(self):
        self.current_word = choice(list(words.keys()))
        pass

    def count_points(self, answer_time):
        # pattern = '%H:%M:%S'
        # int(mktime(strptime(answer_time, pattern)))
        return 10

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
            'PLAYER_INIT': self.get_new_user_requests,
            'GAME_INIT': None
        }
        self.game_logic = GameLogic()
        self.current_drawing = None
        self.current_drawing_it = 0
        self.points = dict()


    def start_round(self):
        self.game_logic.start_time = datetime.now()
        self.game_logic.set_random_current_word()
        
        self.current_drawing_it = (self.current_drawing_it + 1) % len(self.clients.d)
        self.current_drawing = self.clients.get_all_usernames()[self.current_drawing_it]

    def get_new_user_requests(self, request):
        requests = list()
        if len(self.clients.d) == 1:
            self.start_round()
        
        requests.append(self.get_current_word_request(request))
        requests.append(self.get_points_request())
        return requests


    def get_new_round_request(self):
        drawing_player_r = Request()
        other_players_r = Request()

        drawing_player_r.headers['Action'] = 'NEW_ROUND'
        other_players_r.headers['Action'] = 'NEW_ROUND'
        other_players_r.headers['Users'] = ''
        
        for client in self.clients.get_all_usernames():
            if client == self.current_drawing:
                drawing_player_r.headers['Users'] = client
            else:
                other_players_r.headers['Users'] += (client + ', ')
                other_players_data = {
                    'message': self.game_logic.current_word_underlines()
                }

        self.get_current_word_request()        
        drawing_player_r.headers['Data'] = json.dumps(drawing_player_data)
        other_players_r.headers['Data'] = json.dumps(other_players_data)
        return [ drawing_player_r, other_players_r ]


    def get_current_word_request(self, request):
        r = Request()
        r.headers['Action'] = 'CURRENT_WORD'

        if request.user == self.current_drawing:
            data = {
                'message': self.game_logic.current_word
            }
        else:
            data = {
                'message': self.game_logic.current_word_underlines()
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
        message = data['message']

        requests = list()
        requests.append(self.get_current_word_request(request))

        result, points = self.game_logic.answer_result(message)
        if result:
            requests.append(self.get_message_request(f'{user}: Answer correct!'))
            self.points[user] += points
            requests.append(self.get_points_request())
            requests.append(self.get_message_request(f'New round, {self.current_drawing} is drawing'))

            print(self.current_drawing)
            self.start_round()
            print(self.current_drawing)
            requests.extend(self.get_new_round_request())
        else:
            requests.append(self.get_message_request(f'{user}: {message}'))

        return requests

    def send_draw(self, request: Request):
        if self.current_drawing == request.user:
            r = Request()
            r.headers['Action'] = 'DRAW'
            r.headers['Data'] = json.dumps(request.data)
            return [r]
        else:
            return []

    def dispatch(self, request: Request) -> tp.List[Request]:
        action = request.action
        function = self.dispatcher.get(action)
        if function is not None:
            return function(request)

        return []
