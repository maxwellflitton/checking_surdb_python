import uuid
from typing import Optional, Any, Dict

import aiohttp
import json

from surrealdb.connections.async_template import AsyncTemplate
from surrealdb.connections.url import Url
from surrealdb.connections.utils_mixin import UtilsMixin
from surrealdb.request_message.message import RequestMessage
from surrealdb.request_message.methods import RequestMethod


class AsyncHttpSurrealConnection(AsyncTemplate, UtilsMixin):
    """
    A single async connection to a SurrealDB instance using HTTP. To be used once and discarded.

    # Notes
    A new HTTP session is created for each query to send a request to the SurrealDB server.

    Attributes:
        url: The URL of the database to process queries for.
        max_size: The maximum size of the connection payload.
        id: The ID of the connection.
    """

    def __init__(
        self,
        url: str,
    ) -> None:
        """
        Constructor for the AsyncHttpSurrealConnection class.

        :param url: (str) The URL of the database to process queries for.
        """
        self.raw_url: str = url.rstrip("/")
        self.url: Url = Url(url)
        self.host: str = self.url.hostname
        self.port: Optional[int] = self.url.port
        self.id: str = str(uuid.uuid4())
        self.token: Optional[str] = None

    async def _send(
        self,
        message: RequestMessage,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Sends an HTTP request to the SurrealDB server.

        :param endpoint: (str) The endpoint of the SurrealDB API to send the request to.
        :param method: (str) The HTTP method (e.g., "POST", "GET", "PUT", "DELETE").
        :param headers: (dict) Optional headers to include in the request.
        :param payload: (dict) Optional JSON payload to include in the request body.

        :return: (dict) The decoded JSON response from the server.
        """
        json_body, method, endpoint = message.JSON_HTTP_DESCRIPTOR
        url = f"{self.raw_url}/{endpoint.lstrip('/')}"
        headers = headers or {}
        headers["Accept"] = "application/json"
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        async with aiohttp.ClientSession() as session:
             async with session.request(
                method=method.value,
                url=url,
                headers=headers,
                json=json.dumps(json_body),
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                response.raise_for_status()
                response = await response.json()
                # self.check_response_for_error(response)
                return response

    def set_token(self, token: str) -> None:
        """
        Sets the token for authentication.

        :param token: (str) The token to use for the connection.
        """
        self.token = token

    async def signin(self, params: dict) -> dict:
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
            username=params.get("username"),
            password=params.get("password"),
            # account=params.get("namespace"),
            # database=params.get("database"),
            # namespace=params.get("namespace"),
        )
        # Send the request using the _send method with kwargs as the payload.
        outcome = await self._send(message=message)
        self.check_response_for_result(outcome, "sigin")
        return outcome


