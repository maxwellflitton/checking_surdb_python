from unittest import TestCase, main, IsolatedAsyncioTestCase

from surrealdb.request_message.message import RequestMessage
from surrealdb.request_message.methods import RequestMethod
from surrealdb.connections.async_ws import AsyncWsSurrealConnection


class TestAsyncWsSurrealConnection(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.url = "ws://localhost:8000"
        self.password = "root"
        self.username = "root"
        self.vars_params = {
            "username": self.username,
            "password": self.password,
        }
        self.database_name = "test_db"
        self.namespace = "test_ns"

    # async def test_signup_namespace(self):
    #     connection = AsyncWsSurrealConnection(self.url)
    #     await connection.query("")
    #     outcome = await connection.signup(vars={
    #         "namespace": self.namespace,
    #         "database": self.database_name,
    #         "variables": {
    #
    #         }
    #     })
    #
    #
    #     await connection.socket.close()


if __name__ == "__main__":
    main()
