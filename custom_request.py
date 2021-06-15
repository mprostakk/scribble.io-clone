from json import loads


class Request:
    def __init__(self):
        self.headers = dict()
        self.DATA_HEADER_NAME = 'Data'
        self.user = None
        self.users_to_send = list()

    @property
    def data(self) -> str:
        return self.headers.get(self.DATA_HEADER_NAME)

    @property
    def action(self) -> str:
        return self.headers.get('Action')

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

            if self.DATA_HEADER_NAME in header:
                self.parse_data_header(header)
                continue

            name, data = header.split(': ')
            self.headers[name] = data

    def parse_data_header(self, header):
        json_data = header.split(f'{self.DATA_HEADER_NAME}: ')[1]
        data = loads(json_data)
        self.headers[self.DATA_HEADER_NAME] = data
