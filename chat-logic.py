# if received new message propagate it forward and send points info if required
# Action: ANSWEAR_RESULT
# User: username
# Content-Length: 30
# Data: "{"message": "message_from_user", 
#         "result": "true",
#         "timeStamp": "hh:mm:ss",
#         "points": "0-100",
#        }"



# if answer changes points, send UPDATE_PLAYERS
# Action: UPDATE_PLAYERS                                     \r\n
# Data: "{"player_list": [{"maciej": 90}, {"malika": 100}]}" \r\n


# MOCK
# received message
# Action: SEND_MESSAGE
# User: username
# Content-Length: 90
# Data: "{"message": "data", "timeStamp": "HH:MM:SS"}"



class User:
    def __init__(self) -> None:
        self.username = None
        self.user_id = None

users = list()
user1 = User()
user2 = User()
user1.username, user1.user_id = 'malika', 0
user2.username, user2.user_id = 'maciek', 1
users.append(user1)
users.append(user2)

# global var with current guess word
current_word = 'apple'

def detect_answer(message):
    pass