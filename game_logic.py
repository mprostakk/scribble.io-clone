from words_list import words
from time import mktime, strptime
from custom_request import Request

MAX_TIME = 120
# points [50, 40, ]

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
        data = message['message']
        # time = message['timeStamp']
        time = ''
        is_answer = self.detect_answer(data)
        if is_answer:
            points = self.count_points(time)
            return is_answer, points
        else:
            return is_answer, 0

class Game:
    def __init__(self):
        self.dispatcher = {
            'DRAW': self.send_draw,
            'SEND_MESSAGE': self.send_message,
        }
        self.game_logic = GameLogic()
        # self.players = tp.List[Player]
        # self.current_drawing = Player

    def send_draw(self, request: Request):
        return

    def send_message(self, request: Request):
        data = request.data
        user = request.user

        requests = list()

        result, points = self.game_logic.answer_result(data)
        if result:
            # Save them to user with username = user
            r = Request()
            r.headers['Action'] = 'UPDATE_CHAT'
            r.headers['Data'] = f'user: {user} - Answer correct'
            requests.append(r)

            r2 = Request()
            r2.headers['Action'] = 'UPDATE_POINTS'
            r2.headers['Data'] = 'malika: 20, maciej: 10'
            requests.append(r2)

            print("Answer correct | [POINTS] -> ", points)
        else:
            r = Request()
            r.headers['Action'] = 'UPDATE_CHAT'
            r.headers['Data'] = f'user: {user} - {data}'
            requests.append()

            print("Answer incorrect | [POINTS] -> ", points)
        
        return requests

    def dispatch(self, request: Request) -> tp.List[Request]:
        action = request.action
        function = self.dispatcher.get(action)
        if function is not None:
            return function(request)
        
        return []
