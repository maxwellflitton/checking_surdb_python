from unittest import TestCase, main, IsolatedAsyncioTestCase

from surrealdb.request_message.message import RequestMessage
from surrealdb.request_message.methods import RequestMethod
from surrealdb.connections.async_ws import AsyncWsSurrealConnection


class TestAsyncWsSurrealConnection(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.url = "ws://localhost:8000"
        self.password = "root"
        self.username = "root"
        self.database_name = "test_db"
        self.namespace = "test_ns"
        self.connection = AsyncWsSurrealConnection(self.url)
        _ = await self.connection.signin(self.username, self.password)
        _ = await self.connection.use(namespace=self.namespace, database=self.database_name)

    async def test_info(self):
        outcome = await self.connection.info()
        #  TODO => confirm that the info is what we expect
        print(outcome)


if __name__ == "__main__":
    main()
