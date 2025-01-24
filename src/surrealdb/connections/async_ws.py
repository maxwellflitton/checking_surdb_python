"""
A basic async connection to a SurrealDB instance.
"""
import uuid
from typing import Optional, Any, Dict, Union, List

import websockets

from surrealdb.connections.async_template import AsyncTemplate
from surrealdb.connections.url import Url
from surrealdb.data.cbor import decode
from surrealdb.request_message.message import RequestMessage
from surrealdb.request_message.methods import RequestMethod
from surrealdb.data.types.record_id import RecordID
from surrealdb.data.types.table import Table


class AsyncWsSurrealConnection(AsyncTemplate):
    """
    A single async connection to a SurrealDB instance. To be used once and discarded.

    # Notes
    A new connection is created for each query. This is because the async websocket connection is
    dropped

    Attributes:
        url: The URL of the database to process queries for.
        user: The username to login on.
        password: The password to login on.
        namespace: The namespace that the connection will stick to.
        database: The database that the connection will stick to.
        max_size: The maximum size of the connection.
        id: The ID of the connection.
    """
    def __init__(
            self,
            url: str,
            max_size: int = 2 ** 20,
    ) -> None:
        """
        The constructor for the AsyncSurrealConnection class.

        :param host: (str) the url of the database to process queries for
        :param port: (int) the port that the database is listening on
        :param user: (str) the username to login on
        :param password: (str) the password to login on
        :param namespace: (str) the namespace that the connection will stick to
        :param database: (str) The database that the connection will stick to
        :param max_size: (int) The maximum size of the connection
        :param encrypted: (bool) Whether the connection is encrypted
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
            raise Exception(f"error {process}: {response.get('error')}")

    @staticmethod
    def check_response_for_result(response: dict, process: str) -> None:
        if response.get("result") is None:
            raise Exception(f"no result {process}: {response}")

    async def _send(self, message: RequestMessage, process: str) -> dict:
        if self.socket is None:
            self.socket = await websockets.connect(
                self.raw_url,
                max_size=self.max_size,
                subprotocols=[websockets.Subprotocol("cbor")]
            )
        await self.socket.send(message.WS_CBOR_DESCRIPTOR)
        response = decode(await self.socket.recv())
        self.check_response_for_error(response, process)
        return response

    # async def signup(self, vars: Dict[str, Any]) -> str:

    async def signin(self, vars: Dict[str, Any]) -> str:
        """
        Signs in to the SurrealDB instance.

        :return: None
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
        response = await self._send(message, "signing in")
        self.check_response_for_result(response, "signing in")
        self.token = response["result"]
        if response.get("id") is None:
            raise Exception(f"no id signing in: {response}")
        self.id = response["id"]

    async def query(self, query: str, params: Optional[dict] = None) -> dict:
        if params is None:
            params = {}
        message = RequestMessage(
            self.id,
            RequestMethod.QUERY,
            query=query,
            params=params,
        )
        response = await self._send(message, "query")
        self.check_response_for_result(response, "query")
        return response["result"][0]["result"]

    async def use(self, namespace: str, database: str) -> None:
        message = RequestMessage(
            self.id,
            RequestMethod.USE,
            namespace=namespace,
            database=database,
        )
        await self._send(message, "use")

    async def info(self):
        message = RequestMessage(
            self.id,
            RequestMethod.INFO
        )
        return await self._send(message, "getting database information")

    async def version(self) -> str:
        message = RequestMessage(
            self.id,
            RequestMethod.VERSION
        )
        response = await self._send(message, "getting database version")
        self.check_response_for_result(response, "getting database version")
        return response["result"]

    async def authenticate(self, token: str) -> dict:
        message = RequestMessage(
            self.id,
            RequestMethod.AUTHENTICATE,
            token=token
        )
        return await self._send(message, "authenticating")

    async def invalidate(self) -> dict:
        message = RequestMessage(self.id, RequestMethod.INVALIDATE)
        return await self._send(message, "invalidating")

    async def let(self, key: str, value: Any) -> None:
        message = RequestMessage(
            self.id,
            RequestMethod.LET,
            key=key,
            value=value
        )
        await self._send(message, "letting")

    async def unset(self, key: str) -> None:
        message = RequestMessage(
            self.id,
            RequestMethod.UNSET,
            params=[key]
        )
        await self._send(message, "unsetting")

    async def select(self, thing: str) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.SELECT,
            params=[thing]
        )
        response = await self._send(message, "select")
        self.check_response_for_result(response, "select")
        return response["result"]

    async def create(
            self,
            thing: Union[str, RecordID, Table],
            data: Optional[Union[Union[List[dict], dict], dict]] = None,
    ) -> Union[List[dict], dict]:
        message = RequestMessage(
            self.id,
            RequestMethod.CREATE,
            collection=thing,
            data=data
        )
        response = await self._send(message, "create")
        self.check_response_for_result(response, "create")
        return response["result"]

    async def update(
            self, thing: str, data: Optional[Dict[str, Any]]
    ) -> Union[List[dict], dict]:
        pass


    # async def set_space(self, socket) -> None:
    #     """
    #     Sets the namespace and database for the connection.
    #
    #     :return: None
    #     """
    #     # await socket.send(json.dumps(self.use_params, ensure_ascii=False))
    #     # _ = json.loads(await socket.recv())
    #     await socket.send(encode(self.use_params))
    #     _ = decode(await socket.recv())
    #
    # async def query(self, query: str, vars: Optional[Dict[str, Any]] = None) -> dict:
    #     """
    #     Queries the SurrealDB instance.
    #
    #     :param query: The query to run
    #     :param vars: The variables to use in the query
    #     :return: The result of the query
    #     """
    #     query = Query(query, vars)
    #
    #     async with websockets.connect(self.url, max_size=self.max_size, subprotocols=[websockets.Subprotocol("cbor")]) as websocket:
    #         # login and unset the space
    #         await self.signin(websocket)
    #         await self.set_space(websocket)
    #
    #         # send and receive the query
    #         await websocket.send(encode(query.query_params))
    #         response = decode(await websocket.recv())
    #         if response.get("result") is None:
    #             raise Exception(f"error querying no result: {response}")
    #         response = response["result"]
    #         if response[0].get("status") is not None and response[0].get("status") == "ERR":
    #             raise Exception(f"error querying: {response[0].get('result')}")
    #     return response[0]["result"]
    #
    # @property
    # def sign_params(self) -> dict:
    #     return {
    #         "id": self.id,
    #         "method": "signin",
    #         "params": [
    #             {
    #                 "user": self.user,
    #                 "pass": self.password
    #             }
    #         ]
    #     }
    #
    # @property
    # def use_params(self) -> dict:
    #     return {
    #         "id": self.id,
    #         "method": "use",
    #         "params": [
    #             self.namespace,
    #             self.database
    #         ]
    #     }