from unittest import main, IsolatedAsyncioTestCase
from surrealdb.connections.async_http import AsyncHttpSurrealConnection
from surrealdb.request_message.methods import RequestMethod
from surrealdb.request_message.message import RequestMessage


class TestAsyncHttpSurrealConnection(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.url = "http://localhost:8000"
        self.password = "root"
        self.username = "root"
        self.database_name = "test_db"
        self.namespace = "test_ns"
        self.vars_params = {
            "username": self.username,
            "password": self.password,
        }

    async def test_signin_root(self):
        connection = AsyncHttpSurrealConnection(self.url)
        outcome = await connection.signin(self.vars_params)
        self.assertIn("token", outcome)  # Check that the response contains a token

    async def test_signin_namespace(self):
        connection = AsyncHttpSurrealConnection(self.url)
        _ = await connection.signin(self.vars_params)
        _ = await connection.use(namespace=self.namespace, database=self.database_name)
        # TODO => it errors if "namespace" is present
        # self.vars_params["namespace"] = self.namespace
        self.vars_params["database"] = self.database_name
        _ = await connection.signin(self.vars_params)


if __name__ == "__main__":
    main()
