from enum import Enum

class APIErrorType(str, Enum):
    CRITICAL = "CRITICAL"
    BUSINESS = "BUSINESS"


class APIError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.code = kwargs.get("code", 400)
        self.type = kwargs.get("type", APIErrorType.CRITICAL)
        self.payload = kwargs.get("payload", None)
        self.message = kwargs.get("message", "Unknown error") if len(args) == 0 else args[0]

    def cause(self) -> Exception:
        return self

    def __str__(self):
        return self.message

    
class WrappedAPIError(APIError):
    def __init__(self, cause, *args, **kwargs):
        super(WrappedAPIError, self).__init__(*args, **kwargs)
        self._cause = cause

    def cause(self) -> Exception:
        return self._cause


class MissingAttribute(APIError):
    def __init__(self, attribute, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attribute = attribute
        self.message = f'Missing required attribute "{self.attribute}"'