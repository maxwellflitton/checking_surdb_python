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

    async def test_signin_root(self):
        connection = AsyncWsSurrealConnection(self.url)
        _ = await connection.signin(self.vars_params)
        await connection.socket.close()

    async def test_signin_namespace(self):
        connection = AsyncWsSurrealConnection(self.url)
        _ = await connection.signin(self.vars_params)
        _ = await connection.use(namespace=self.namespace, database=self.database_name)
        # TODO => it errors if "namespace" is present
        # self.vars_params["namespace"] = self.namespace
        self.vars_params["database"] = self.database_name
        _ = await connection.signin(self.vars_params)
        await connection.socket.close()

    async def test_signin_database(self):
        # create database
        pass

    async def test_signin_with_record_access(self):
        # create a table that has records of the users (name the table user)

        # create a user

        # signin with record access
        #
        pass



if __name__ == "__main__":
    main()
