from json import loads


class Request:
    def __init__(self):
        self.headers = dict()
        self.DATA_HEADER_NAME = 'Data'
        self.USERS_HEADER_NAME = 'Users'
        self.user = None
        self.users_to_send = list()

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
# POPRAWIĆ
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
        return True if check else False

    def parse_users_header(self, header):
        self.users_to_send.clear()
        usernames: list = header.split(f'{self.USERS_HEADER_NAME}: ')[1].split(', ')
        self.users_to_send.extend(usernames)
        

    def parse_data_header(self, header):
        json_data = header.split(f'{self.DATA_HEADER_NAME}: ')[1]
        data = loads(json_data)
        self.headers[self.DATA_HEADER_NAME] = data


class DrawRequest(Request):
    def __init__(self):
        self.x = None
        self.y = None
        self.color = None

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


class MessageRequest(Request):
    def __init__(self):
        self.message = ''

    @property
    def get_message(self):
        return self.message
        
    def parse_message(self):
        self.message = self.headers.get('Message')
