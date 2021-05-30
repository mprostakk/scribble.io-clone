from json import loads
class Request:
    def __init__(self):
        self.headers = dict()

    @property
    def data(self) -> str:
        return self.headers.get('Data')

    @property
    def action(self) -> str:
        return self.headers.get('Action')

    @property
    def user(self) -> str:
        return self.headers.get('User')

    @property
    def to_user(self) -> str:
        return self.headers.get('To_users', 'ALL')

    def parse_headers():
        pass

    def parse_request(self, data: str) -> None:
        stripped_data = data[:-2].split('\r\n')
        for header in stripped_data:

            if header == '':
                continue

            if 'Data' in header:
                name = 'Data'
                json_data = header.split('Data: ')[1]
                data = loads(json_data)
                self.headers[name] = data
                continue

            name, data = header.split(': ')
            self.headers[name] = data

        print(self.headers)
