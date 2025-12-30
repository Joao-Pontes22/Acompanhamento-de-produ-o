

class HttpException(Exception):
    """Base class for HTTP exceptions."""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

class NotFoundException(Exception):
    def __init__(self, entity: str):
        super().__init__(f"{entity} not found")