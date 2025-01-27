from unittest import TestCase, main

from surrealdb.connections.blocking_ws import BlockingWsSurrealConnection


class TestBlockingWsSurrealConnection(TestCase):

    def setUp(self):
        self.url = "ws://localhost:8000"
        self.password = "root"
        self.username = "root"
        self.vars_params = {
            "username": self.username,
            "password": self.password,
        }
        self.database_name = "test_db"
        self.namespace = "test_ns"

    def test_signin_root(self):
        connection = BlockingWsSurrealConnection(self.url)
        connection.signin(self.vars_params)
        if connection.socket:
            connection.socket.close()

    def test_signin_namespace(self):
        connection = BlockingWsSurrealConnection(self.url)
        connection.signin(self.vars_params)
        connection.use(namespace=self.namespace, database=self.database_name)
        # TODO => it errors if "namespace" is present
        # self.vars_params["namespace"] = self.namespace
        self.vars_params["database"] = self.database_name
        connection.signin(self.vars_params)
        if connection.socket:
            connection.socket.close()

    def test_signin_database(self):
        # Create database
        pass

    def test_signin_with_record_access(self):
        # Create a table that has records of the users (name the table user)

        # Create a user

        # Sign in with record access
        pass


if __name__ == "__main__":
    main()
