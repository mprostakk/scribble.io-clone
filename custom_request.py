from json import loads
from uuid import uuid4
from exceptions import ERROR_CODES, ServerErrorException

class Request:
    def __init__(self):
        self.headers = dict()
        self.DATA_HEADER_NAME = 'Data'
        self.USERS_HEADER_NAME = 'Users'
        self.user = None
        self.users_to_send = list()
        self.session_id = None

    @staticmethod
    def create_from_base(self, request):
        raise NotImplementedError

    @property
    def data(self) -> str:
        return self.headers.get(self.DATA_HEADER_NAME)

    @property
    def action(self) -> str:
        return self.headers.get('Action')

    @property
    def users(self) -> str:
        return self.headers.get('Users')

    @property
    def to_users(self) -> list:
        return self.users_to_send

    def init_session_id(self):
        self.session_id = uuid4()

    def parse_headers(self) -> str:
        s = ''
        for key, value in self.headers.items():
            s += f'{key}: {value}\r\n'

        s += '\r\n'
        return s

    def parse_request(self, data: str) -> None:
        stripped_data = data[:-2].split('\r\n')
        for header in stripped_data:

            if header == '':
                continue
            if self.detect_headers(header):
                continue

            name, data = header.split(': ')
            self.headers[name] = data


    def detect_headers(self, header):
        check = False
        if self.DATA_HEADER_NAME in header:
            check = True
            self.parse_data_header(header)
        if self.USERS_HEADER_NAME in header:
            check = True
            self.parse_users_header(header)
        return check

    def parse_users_header(self, header):
        self.users_to_send.clear()
        usernames: list = header.split(f'{self.USERS_HEADER_NAME}: ')[1].split(', ')
        self.users_to_send.extend(usernames)

    def parse_data_header(self, header):
        json_data = header.split(f'{self.DATA_HEADER_NAME}: ')[1]
        data = loads(json_data)
        self.headers[self.DATA_HEADER_NAME] = data

 
class ContentTypeJsonMixin:
    def content_type(self):
        return 'json'


class ContentLengthMixin:
    def get_content_length(self):
        return len(self.headers.get('Data'))

    def validate_content_length(self) -> bool:
        return int(self.headers.get('Content-Length')) == self.get_content_length()

class DrawRequest(Request, ContentTypeJsonMixin, ContentLengthMixin):
    def __init__(self):
        super().__init__()

        self.x = None
        self.y = None
        self.color = None
        self.headers['Action'] = 'DRAW'

    @property
    def get_color(self):
        return self.color
    
    @property
    def get_x(self):
        return self.x
    
    @property
    def get_y(self):
        return self.y
    
    def parse_draw(self):
        self.x = self.headers.get('X')
        self.y = self.headers.get('Y')
        self.color = self.headers.get('Color')
    
    def parse_from_base(self, request):
        self.headers = request.headers

    def validate(self):
        pass


class MessageRequest(Request, ContentTypeJsonMixin, ContentLengthMixin):
    def __init__(self):     
        super().__init__()
        self.message = ''
        self.headers['Action'] = 'UPDATE_CHAT'
        self.user_session_id = None
        self.data_length = -1
        

    def set_data_length(self):
        self.data_length = len(self.message) 

    @property
    def get_message(self):
        return self.message
        
    def parse_message(self):
        self.message = self.headers.get('Message')

    def parse_from_base(self, request):
        self.headers = request.headers
    
    def validate(self):
        pass


class CurrentWordRequest(Request, ContentTypeJsonMixin, ContentLengthMixin):
    def __init__(self):     
        super().__init__()
        self.message = ''
        self.headers['Action'] = 'CURRENT_WORD'
        self.data_length = -1

    def parse_message(self):
        self.message = self.headers.get('Message')

    def parse_from_base(self, request):
        self.headers = request.headers

    def set_data_length(self):
        self.data_length = len(self.message) 
        
    @property
    def get_message(self):
        return self.message
        
