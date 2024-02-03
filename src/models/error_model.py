class ErrorModel:
    def __init__(self, error_title, error_message):
        self._error_title = error_title
        self._error_message = error_message

    @property
    def error_title(self):
        return self._error_title
    
    @property
    def error_message(self):
        return self._error_message