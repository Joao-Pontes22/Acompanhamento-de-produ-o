

class HttpException(Exception):
    """Base class for HTTP exceptions."""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

class NotFoundException(Exception):
    def __init__(self, entity: str):
        super().__init__(f"{entity} not found")


class AlreadyExist(Exception):
    def __init__(self, entity: str):
        super().__init__(f"{entity} already exist")

class InvalidNameException(Exception):
    pass

class IncorrectPasswordException(Exception):
    def __init__(self):
        super().__init__("Password incorrect")

class StockInssuficientException(Exception):
    def __init__(self, part_number: str, required: int, available: int):
        super().__init__(f"Insufficient stock for part number {part_number}: required {required}, available {available}")