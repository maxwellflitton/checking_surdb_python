"""
A basic blocking connection to a SurrealDB instance.
"""
import uuid
from typing import Optional, Any, Dict, Union, List
from uuid import UUID

import websockets.sync.client as ws_sync
import websockets

from surrealdb.connections.sync_template import SyncTemplate
from surrealdb.connections.url import Url
from surrealdb.data.cbor import decode
from surrealdb.request_message.message import RequestMessage
from surrealdb.request_message.methods import RequestMethod
from surrealdb.data.types.record_id import RecordID
from surrealdb.data.types.table import Table


class BlockingWsSurrealConnection(SyncTemplate):
    """
    A single blocking connection to a SurrealDB instance. To be used once and discarded.

    # Notes
    A new connection is created for each query. This is because the WebSocket connection is
    dropped after the query is completed.

    Attributes:
        url: The URL of the database to process queries for.
        user: The username to login on.
        password: The password to login on.
        namespace: The namespace that the connection will stick to.
        database: The database that the connection will stick to.
        max_size: The maximum size of the connection.
        id: The ID of the connection.
    """

    def __init__(self, url: str, max_size: int = 2 ** 20) -> None:
        """
        The constructor for the BlockingWsSurrealConnection class.

        :param url: (str) the URL of the database to process queries for.
        :param max_size: (int) The maximum size of the connection.
        """
        self.raw_url: str = f"{url}/rpc"
        self.url: Url = Url(url)
        self.host: str = self.url.hostname
        self.port: int = self.url.port
        self.max_size: int = max_size
        self.id: str = str(uuid.uuid4())
        self.token: Optional[str] = None
        self.socket = None

    @staticmethod
    def check_response_for_error(response: dict, process: str) -> None:
        if response.get("error") is not None:
            raise Exception(f"Error {process}: {response.get('error')}")

    @staticmethod
    def check_response_for_result(response: dict, process: str) -> None:
        if response.get("result") is None:
            raise Exception(f"No result {process}: {response}")

    def _send(self, message: RequestMessage, process: str) -> dict:
        if self.socket is None:
            self.socket = ws_sync.connect(
                self.raw_url,
                max_size=self.max_size,
                subprotocols=[websockets.Subprotocol("cbor")],
            )
        self.socket.send(message.WS_CBOR_DESCRIPTOR)
        response = decode(self.socket.recv())
        self.check_response_for_error(response, process)
        return response

    def signin(self, vars: Dict[str, Any]) -> str:
        """
        Signs in to the SurrealDB instance.
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
        if response.get("id") is None:
            raise Exception(f"No ID signing in: {response}")
        self.id = response["id"]

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

    def use(self, namespace: str, database: str) -> None:
        message = RequestMessage(
            self.id,
            RequestMethod.USE,
            namespace=namespace,
            database=database,
        )
        self._send(message, "use")

    def info(self) -> dict:
        message = RequestMessage(
            self.id,
            RequestMethod.INFO
        )
        return self._send(message, "getting database information")

    def version(self) -> str:
        message = RequestMessage(
            self.id,
            RequestMethod.VERSION
        )
        response = self._send(message, "getting database version")
        self.check_response_for_result(response, "getting database version")
        return response["result"]

    def authenticate(self, token: str) -> dict:
        message = RequestMessage(
            self.id,
            RequestMethod.AUTHENTICATE,
            token=token
        )
        return self._send(message, "authenticating")

    def invalidate(self) -> None:
        message = RequestMessage(self.id, RequestMethod.INVALIDATE)
        self._send(message, "invalidating")

    def let(self, key: str, value: Any) -> None:
        message = RequestMessage(
            self.id,
            RequestMethod.LET,
            key=key,
            value=value
        )
        self._send(message, "letting")

    def unset(self, key: str) -> None:
        message = RequestMessage(
            self.id,
            RequestMethod.UNSET,
            params=[key]
        )
        self._send(message, "unsetting")

    def select(self, thing: str) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.SELECT,
            params=[thing]
        )
        response = self._send(message, "select")
        self.check_response_for_result(response, "select")
        return response["result"]

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

    def live(self, table: Union[str, Table], diff: bool = False) -> UUID:
        message = RequestMessage(
            self.id,
            RequestMethod.LIVE,
            table=table,
        )
        response = self._send(message, "live")
        self.check_response_for_result(response, "live")
        return response["result"]

    def kill(self, query_uuid: Union[str, UUID]) -> None:
        message = RequestMessage(
            self.id,
            RequestMethod.KILL,
            uuid=query_uuid
        )
        self._send(message, "kill")

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
