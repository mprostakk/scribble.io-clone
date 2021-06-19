ERROR_DESCRIPTIONS = {
    401: 'Authorization Failed - session_id unknown',
    400: 'Syntax Error - could not parse incoming request',
    403: 'Date Length doesn`t match Content Length',
    402: 'Unknown Action Type',
    412: 'Points update failed - unknown username',
    500: 'Internal server error'
}


ERROR_CODES = {
    'SYNTAX_ERROR': 400,
    'AUTH_FAILED': 401,
    'CONTENT_LENGTH': 403,
    'UNKNOWN_ACTION_TYPE': 402,
    'FAILED_UPDATE_POINTS': 412,
    'INTERNAL_SERVER_ERROR': 500
}


class ServerErrorException(Exception):
    """Error"""

    def __init__(self, error_type: str, *args, **kwargs):
        self.error_type: str = error_type
        self.error_code = ERROR_CODES[self.error_type]
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f'Error {self.error_type} - {ERROR_DESCRIPTIONS[self.error_code]}'
