from cerberus import Validator

from surrealdb.data.cbor import encode
from surrealdb.request_message.methods import RequestMethod


class WsCborDescriptor:
    def __get__(self, obj, type=None) -> bytes:
        if obj.method == RequestMethod.USE:
            return self.prep_use(obj)
        elif obj.method == RequestMethod.INFO:
            return self.prep_info(obj)
        elif obj.method == RequestMethod.VERSION:
            return self.prep_version(obj)
        elif obj.method == RequestMethod.SIGN_UP:
            return self.prep_signup(obj)
        elif obj.method == RequestMethod.SIGN_IN:
            return self.prep_signin(obj)
        elif obj.method == RequestMethod.AUTHENTICATE:
            return self.prep_authenticate(obj)
        elif obj.method == RequestMethod.INVALIDATE:
            return self.prep_invalidate(obj)
        elif obj.method == RequestMethod.LET:
            return self.prep_let(obj)
        elif obj.method == RequestMethod.UNSET:
            return self.prep_unset(obj)
        elif obj.method == RequestMethod.LIVE:
            return self.prep_live(obj)
        elif obj.method == RequestMethod.KILL:
            return self.prep_kill(obj)
        elif obj.method == RequestMethod.QUERY:
            return self.prep_query(obj)
        elif obj.method == RequestMethod.INSERT:
            return self.prep_insert(obj)
        elif obj.method == RequestMethod.PATCH:
            return self.prep_patch(obj)

        raise ValueError(f"Invalid method for Cbor WS encoding: {obj.method}")

    def _raise_invalid_schema(self, data:dict, schema: dict, method: str) -> None:
        v = Validator(schema)
        if not v.validate(data):
            raise ValueError(f"Invalid schema for Cbor WS encoding for {method}: {v.errors}")

    def prep_use(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": [obj.kwargs.get("namespace"), obj.kwargs.get("database")],
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True},  # "method" must be a string
            "params": {
                "type": "list",  # "params" must be a list
                "schema": {"type": "string"},  # Elements of "params" must be strings
                "required": True
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_info(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True},  # "method" must be a string
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_version(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True},  # "method" must be a string
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_signup(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": [
                {
                    "NS": obj.kwargs.get("namespace"),
                    "DB": obj.kwargs.get("database"),
                    "AC": obj.kwargs.get("account"),
                    "username": obj.kwargs.get("username"),
                    "password": obj.kwargs.get("password"),
                }
            ],
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True},  # "method" must be a string
            "params": {
                "type": "list",  # "params" must be a list
                "schema": {
                    "type": "dict",  # Each element of the "params" list must be a dictionary
                    "schema": {
                        "NS": {"type": "string", "required": True},  # "NS" must be a string
                        "DB": {"type": "string", "required": True},  # "DB" must be a string
                        "AC": {"type": "string", "required": True},  # "AC" must be a string
                        "username": {"type": "string", "required": True},  # "username" must be a string
                        "password": {"type": "string", "required": True},  # "password" must be a string
                    },
                },
                "required": True,
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_signin(self, obj) -> bytes:
        if obj.kwargs.get("namespace") is None:
            # root user signing in
            data = {
                "id": obj.id,
                "method": obj.method.value,
                "params": [
                    {
                        "user": obj.kwargs.get("username"),
                        "pass": obj.kwargs.get("password")
                    }
                ]
            }
        else:
            data = {
                "id": obj.id,
                "method": obj.method.value,
                "params": [
                    {
                        "NS": obj.kwargs.get("namespace"),
                        "DB": obj.kwargs.get("database"),
                        "AC": obj.kwargs.get("account"),
                        "username": obj.kwargs.get("username"),
                        "password": obj.kwargs.get("password")
                    }
                ]
            }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True},
            "params": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "oneof_schema": [
                        {  # First structure for "signin" with "user" and "pass"
                            "user": {"type": "string", "required": True},
                            "pass": {"type": "string", "required": True},
                        },
                        {  # Second structure with "NS", "DB", "AC", "username", and "password"
                            "NS": {"type": "string", "required": True},
                            "DB": {"type": "string", "required": True},
                            "AC": {"type": "string", "required": True},
                            "username": {"type": "string", "required": True},
                            "password": {"type": "string", "required": True},
                        },
                    ],
                },
                "required": True,
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_authenticate(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": [
                obj.kwargs.get("token")
            ]
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True, "allowed": ["authenticate"]},
            "params": {
                "type": "list",
                "schema": {
                    "type": "string",
                    "regex": r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$",  # Matches JWT format
                },
                "required": True,
                "minlength": 1,
                "maxlength": 1,  # Ensures exactly one token in the list
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_invalidate(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True}
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_let(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": [obj.kwargs.get("key"), obj.kwargs.get("value")]
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True, "allowed": ["let"]},
            "params": {
                "type": "list",
                "minlength": 2,
                "required": True
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_unset(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": obj.kwargs.get("params")
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True, "allowed": ["unset"]},
            "params": {
                "type": "list",
                "required": True
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_live(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": obj.kwargs.get("params")
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True, "allowed": ["live"]},
            "params": {
                "type": "list",
                "required": True
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_kill(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": [obj.kwargs.get("uuid")]
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True, "allowed": ["kill"]},
            "params": {
                "type": "list",
                "schema": {"type": "string"},
                "required": True
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_query(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": [
                obj.kwargs.get("query"),
                obj.kwargs.get("params", dict())
            ]
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True, "allowed": ["query"]},
            "params": {
                "type": "list",
                "minlength": 2,  # Ensures there are at least two elements
                "maxlength": 2,  # Ensures exactly two elements
                "required": True
            },
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_insert(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": [
                obj.kwargs.get("collection"),
                obj.kwargs.get("params")
            ]
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True, "allowed": ["insert"]},
            "params": {
                "type": "list",
                "minlength": 2,  # Ensure there are at least two elements
                "maxlength": 2,  # Ensure exactly two elements
                "required": True
            }
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)

    def prep_patch(self, obj) -> bytes:
        data = {
            "id": obj.id,
            "method": obj.method.value,
            "params": [
                obj.kwargs.get("collection"),
                obj.kwargs.get("params")
            ]
        }
        schema = {
            "id": {"required": True},
            "method": {"type": "string", "required": True, "allowed": ["patch"]},
            "params": {
                "type": "list",
                "minlength": 2,  # Ensure there are at least two elements
                "maxlength": 2,  # Ensure exactly two elements
                "required": True,
            }
        }
        self._raise_invalid_schema(data=data, schema=schema, method=obj.method.value)
        return encode(data)
