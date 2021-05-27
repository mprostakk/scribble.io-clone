
class Request:
    def __init__(self):
        self.headers = dict()

    def parse_request(self, data: str) -> None:
        stripped_data = data[:-2].split('\r\n')
        for header in stripped_data:
            if header == '':
                continue

            name, data = header.split(': ')
            self.headers[name] = data
