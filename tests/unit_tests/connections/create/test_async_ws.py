from unittest import main, IsolatedAsyncioTestCase

from surrealdb.connections.async_ws import AsyncWsSurrealConnection
from surrealdb.data.types.record_id import RecordID
from surrealdb.data.types.table import Table


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
        self.data = {
            "username": self.username,
            "password": self.password,
        }
        self.connection = AsyncWsSurrealConnection(self.url)
        _ = await self.connection.signin(self.vars_params)
        _ = await self.connection.use(namespace=self.namespace, database=self.database_name)

    async def test_create_string(self):
        await self.connection.query("DELETE user;")
        outcome = await self.connection.create("user")
        self.assertEqual("user", outcome["id"].table_name)

        self.assertEqual(
            len(await self.connection.query("SELECT * FROM user;")),
            1
        )
        await self.connection.query("DELETE user;")
        await self.connection.socket.close()

    async def test_create_string_with_data(self):
        await self.connection.query("DELETE user;")

        outcome = await self.connection.create("user", self.data)
        self.assertEqual("user", outcome["id"].table_name)
        self.assertEqual(self.password, outcome["password"])
        self.assertEqual(self.username, outcome["username"])

        outcome = await self.connection.query("SELECT * FROM user;")
        self.assertEqual(
            len(outcome),
            1
        )
        self.assertEqual("user", outcome[0]["id"].table_name)
        self.assertEqual(self.password, outcome[0]["password"])
        self.assertEqual(self.username, outcome[0]["username"])

        await self.connection.query("DELETE user;")
        await self.connection.socket.close()

    async def test_create_record_id(self):
        await self.connection.query("DELETE user;")

        record_id = RecordID("user",1)
        outcome = await self.connection.create(record_id)
        self.assertEqual("user", outcome["id"].table_name)
        self.assertEqual(1, outcome["id"].id)

        self.assertEqual(
            len(await self.connection.query("SELECT * FROM user;")),
            1
        )

        await self.connection.query("DELETE user;")
        await self.connection.socket.close()

    async def test_create_record_id_with_data(self):
        await self.connection.query("DELETE user;")

        record_id = RecordID("user", 1)
        outcome = await self.connection.create(record_id, self.data)
        self.assertEqual("user", outcome["id"].table_name)
        self.assertEqual(1, outcome["id"].id)
        self.assertEqual(self.password, outcome["password"])
        self.assertEqual(self.username, outcome["username"])

        outcome = await self.connection.query("SELECT * FROM user;")
        self.assertEqual(
            len(outcome),
            1
        )
        self.assertEqual("user", outcome[0]["id"].table_name)
        self.assertEqual(self.password, outcome[0]["password"])
        self.assertEqual(self.username, outcome[0]["username"])

        await self.connection.query("DELETE user;")
        await self.connection.socket.close()

    async def test_create_table(self):
        await self.connection.query("DELETE user;")

        table = Table("user")
        outcome = await self.connection.create(table)
        self.assertEqual("user", outcome["id"].table_name)

        self.assertEqual(
            len(await self.connection.query("SELECT * FROM user;")),
            1
        )

        await self.connection.query("DELETE user;")
        await self.connection.socket.close()

    async def test_create_table_with_data(self):
        await self.connection.query("DELETE user;")

        table = Table("user")
        outcome = await self.connection.create(table, self.data)
        self.assertEqual("user", outcome["id"].table_name)
        self.assertEqual(self.password, outcome["password"])
        self.assertEqual(self.username, outcome["username"])

        outcome = await self.connection.query("SELECT * FROM user;")
        self.assertEqual(
            len(outcome),
            1
        )
        self.assertEqual("user", outcome[0]["id"].table_name)
        self.assertEqual(self.password, outcome[0]["password"])
        self.assertEqual(self.username, outcome[0]["username"])

        await self.connection.query("DELETE user;")
        await self.connection.socket.close()




if __name__ == "__main__":
    main()
