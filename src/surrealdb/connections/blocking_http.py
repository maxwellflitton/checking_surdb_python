import uuid
from typing import Optional, Any, Dict, Union, List

import requests

from surrealdb.connections.sync_template import SyncTemplate
from surrealdb.connections.url import Url
from surrealdb.connections.utils_mixin import UtilsMixin
from surrealdb.data.cbor import decode
from surrealdb.data.types.record_id import RecordID
from surrealdb.data.types.table import Table
from surrealdb.request_message.message import RequestMessage
from surrealdb.request_message.methods import RequestMethod


class BlockingHttpSurrealConnection(SyncTemplate, UtilsMixin):

    def __init__(self, url: str) -> None:
        self.raw_url: str = url.rstrip("/")
        self.url: Url = Url(url)
        self.host: str = self.url.hostname
        self.port: Optional[int] = self.url.port
        self.token: Optional[str] = None
        self.id: str = str(uuid.uuid4())
        self.namespace: Optional[str] = None
        self.database: Optional[str] = None

    def _send(self, message: RequestMessage, operation: str) -> Dict[str, Any]:
        data = message.WS_CBOR_DESCRIPTOR
        url = f"{self.raw_url}/rpc"
        headers = {
            "Accept": "application/cbor",
            "Content-Type": "application/cbor",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if self.namespace:
            headers["Surreal-NS"] = self.namespace
        if self.database:
            headers["Surreal-DB"] = self.database

        response = requests.post(url, headers=headers, data=data, timeout=30)
        response.raise_for_status()
        raw_cbor = response.content
        data = decode(raw_cbor)
        self.check_response_for_error(data, operation)
        return data

    def set_token(self, token: str) -> None:
        self.token = token

    def signin(self, vars: dict) -> dict:
        """
        Signs in to the SurrealDB instance using the provided credentials and parameters.

        :param kwargs: (dict) A dictionary containing any combination of:
            - username: (str) The username for authentication.
            - password: (str) The password for authentication.
            - namespace: (str) The namespace name.
            - database: (str) The database name.
            - access: (str) Access level (e.g., "user").
            - scope: (str) The scope definition (e.g., "user").
            - variables: (dict) Additional properties required by the access or scope definition.
        :return: (dict) The server's response to the sign-in request.
        """
        message = RequestMessage(
            self.id,
            RequestMethod.SIGN_IN,
            username=vars.get("username"),
            password=vars.get("password"),
            account=vars.get("account"),
            database=vars.get("database"),
            namespace=vars.get("namespace"),
        )
        response = self._send(message, "signing in")
        self.check_response_for_result(response, "signing in")
        self.token = response["result"]
        package = dict()
        package["token"] = self.token
        return package

    def use(self, namespace: str, database: str) -> None:
        message = RequestMessage(
            self.token,
            RequestMethod.USE,
            namespace=namespace,
            database=database,
        )
        data = self._send(message, "use")
        self.namespace = namespace
        self.database = database

    def query(self, query: str, params: Optional[dict] = None) -> dict:
        if params is None:
            params = {}
        message = RequestMessage(
            self.id,
            RequestMethod.QUERY,
            query=query,
            params=params,
        )
        response = self._send(message, "query")
        self.check_response_for_result(response, "query")
        return response["result"][0]["result"]

    def create(
            self,
            thing: Union[str, RecordID, Table],
            data: Optional[Union[Union[List[dict], dict], dict]] = None,
    ) -> Union[List[dict], dict]:
        if isinstance(thing, str):
            if ":" in thing:
                buffer = thing.split(":")
                thing = RecordID(table_name=buffer[0], identifier=buffer[1])
        message = RequestMessage(
            self.id,
            RequestMethod.CREATE,
            collection=thing,
            data=data
        )
        response = self._send(message, "create")
        self.check_response_for_result(response, "create")
        return response["result"]

    def delete(
            self, thing: Union[str, RecordID, Table]
    ) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.DELETE,
            record_id=thing
        )
        response = self._send(message, "delete")
        self.check_response_for_result(response, "delete")
        return response["result"]

    def info(self):
        message = RequestMessage(
            self.id,
            RequestMethod.INFO
        )
        return self._send(message, "getting database information")

    def insert(
            self, table: Union[str, Table], data: Union[List[dict], dict]
    ) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.INSERT,
            collection=table,
            params=data
        )
        response = self._send(message, "insert")
        self.check_response_for_result(response, "insert")
        return response["result"]

    def insert_relation(
            self, table: Union[str, Table], data: Union[List[dict], dict]
    ) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.INSERT_RELATION,
            table=table,
            params=data
        )
        response = self._send(message, "insert_relation")
        self.check_response_for_result(response, "insert_relation")
        return response["result"]

    def invalidate(self) -> None:
        message = RequestMessage(self.id, RequestMethod.INVALIDATE)
        self._send(message, "invalidating")
        self.token = None

    def let(self, key: str, value: Any) -> None:
        message = RequestMessage(
            self.id,
            RequestMethod.LET,
            key=key,
            value=value
        )
        self._send(message, "letting")

    def merge(
            self, thing: Union[str, RecordID, Table], data: Optional[Dict] = None
    ) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.MERGE,
            record_id=thing,
            data=data
        )
        response = self._send(message, "merge")
        self.check_response_for_result(response, "merge")
        return response["result"]

    def patch(
            self, thing: Union[str, RecordID, Table], data: Optional[List[dict]] = None
    ) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.PATCH,
            collection=thing,
            params=data
        )
        response = self._send(message, "patch")
        self.check_response_for_result(response, "patch")
        return response["result"]

    def select(self, thing: str) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.SELECT,
            params=[thing]
        )
        response = self._send(message, "select")
        self.check_response_for_result(response, "select")
        return response["result"]

    def update(
            self,
            thing: Union[str, RecordID, Table],
            data: Optional[Dict] = None
    ) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.UPDATE,
            record_id=thing,
            data=data
        )
        response = self._send(message, "update")
        self.check_response_for_result(response, "update")
        return response["result"]

    def version(self) -> str:
        message = RequestMessage(
            self.id,
            RequestMethod.VERSION
        )
        response = self._send(message, "getting database version")
        self.check_response_for_result(response, "getting database version")
        return response["result"]

    def upsert(
            self, thing: Union[str, RecordID, Table], data: Optional[Dict] = None
    ) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.UPSERT,
            record_id=thing,
            data=data
        )
        response = self._send(message, "upsert")
        self.check_response_for_result(response, "upsert")
        return response["result"]
