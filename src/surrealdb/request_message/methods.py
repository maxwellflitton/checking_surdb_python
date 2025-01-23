from enum import Enum


class RequestMethod(Enum):
    USE = "use"
    SIGN_IN = "signin"
    SIGN_UP = "signup"
    INFO = "info"
    VERSION = "version"
    AUTHENTICATE = "authenticate"
    INVALIDATE = "invalidate"
    LET = "let"
    UNSET = "unset"
    SELECT = "select"
    QUERY = "query"
    CREATE = "create"
    INSERT = "insert"
    PATCH = "patch"
    MERGE = "merge"
    UPDATE = "update"
    UPSERT = "upsert"
    DELETE = "delete"
    LIVE = "live"
    KILL = "kill"

    @staticmethod
    def from_string(method: str) -> "RequestMethod":
        return RequestMethod(method.lower())
