from unittest import TestCase, main, IsolatedAsyncioTestCase

from surrealdb.request_message.message import RequestMessage
from surrealdb.request_message.methods import RequestMethod
from surrealdb.connections.async_ws import AsyncWsSurrealConnection


class TestAsyncWsSurrealConnection(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.url = "ws://localhost:8000"
        self.password = "root"
        self.username = "root"

    async def test_signin(self):
        connection = AsyncWsSurrealConnection(self.url)
        _ = await connection.signin(self.username, self.password)



if __name__ == "__main__":
    main()
