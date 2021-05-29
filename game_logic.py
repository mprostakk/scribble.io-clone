from words_list import words
from time import mktime, strptime

MAX_TIME = 120
# points [50, 40, ]

class GameLogic:
    def __init__(self):
        self.current_word = 'apple'
        self.start_time = None
        pass

    def current_word_setter(self, value):
        self.current_word = value

    def start_time_setter(self, value):
        self.start_time = value.toEpoch()
        
    def count_points(self, answer_time):
        pattern = '%H:%M:%S'
        epoch = int(mktime(strptime(answer_time, pattern)))
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
        time = message['timeStamp']
        is_answer = self.detect_answer(data)
        if is_answer:
            points = self.count_points(time)
            return is_answer, points
        else:
            return is_answer, 0
