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
        self.connection = AsyncWsSurrealConnection(self.url)
        _ = await self.connection.signin(self.vars_params)
        _ = await self.connection.use(namespace=self.namespace, database=self.database_name)
        _ = await self.connection.query("DELETE user;")
        _ = await self.connection.query("REMOVE TABLE user;")
        _ = await self.connection.query(
            "DEFINE TABLE user SCHEMAFULL PERMISSIONS FOR select, update, delete WHERE id = $auth.id;"
            "DEFINE FIELD name ON user TYPE string;"
            "DEFINE FIELD email ON user TYPE string ASSERT string::is::email($value);"
            "DEFINE FIELD password ON user TYPE string;"
            "DEFINE FIELD enabled ON user TYPE bool;"
            "DEFINE INDEX email ON user FIELDS email UNIQUE;"
        )
        _ = await self.connection.query(
            'CREATE user CONTENT {name: "test", email: "test@gmail.com", password: "test", enabled: true};'
        )

    async def test_signup(self):
        vars = {
            "namespace": self.namespace,
            "database": self.database_name,
            "access": "user",
            "variables": {
                "email": "test@gmail.com",
                "password": "test"
            }
        }
        # outcome = await self.connection.query()
        connection = AsyncWsSurrealConnection(self.url)
        outcome = await connection.signup(vars)
        await self.connection.query("DELETE user;")

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
