# Moises Shalimay Andrade
# Auxiliary module with customized error classes

class NotRealNumberError(Exception):
    """Error denoting the input is not a valid integer or float"""

    def __init__(self, message):
        self.message = message 

    def __str__(self):
        if self.message:
            return f"NotRealNumberError:{self.message}"


class InputTypeError(Exception):
    """Error denoting the input is not a valid integer or float"""

    def __init__(self, message):
        self.message = message 

    def __str__(self):
        if self.message:
            return f"InputTypeError:{self.message}"

class TimeConversionError(Exception):
    """"""
    def __init__(self, message):
        self.message = message 

    def __str__(self):
        if self.message:
            return f"pytzFailed:{self.message}"



