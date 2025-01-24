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
            "name": "Jaime",
            "age": 35,
        }
        self.connection = AsyncWsSurrealConnection(self.url)
        _ = await self.connection.signin(self.vars_params)
        _ = await self.connection.use(namespace=self.namespace, database=self.database_name)
        await self.connection.query("DELETE user;")
        await self.connection.query("CREATE user:tobie SET name = 'Tobie';"),

    def check_no_change(self, data: dict):
        record_id = RecordID(table_name="user", identifier="tobie")
        self.assertEqual(record_id, data["id"])
        self.assertEqual('Tobie', data["name"])

    def check_change(self, data: dict):
        record_id = RecordID(table_name="user", identifier="tobie")
        self.assertEqual(record_id, data["id"])

        self.assertEqual('Jaime', data["name"])
        self.assertEqual(35, data["age"])

    async def test_update_string(self):
        outcome = await self.connection.update("user:tobie")
        self.assertEqual(1, len(outcome))
        outcome = await self.connection.query("SELECT * FROM user;")
        self.check_no_change(outcome[0])
        await self.connection.query("DELETE user;")
        await self.connection.socket.close()

    async def test_update_string_with_data(self):
        outcome = await self.connection.update("user:tobie", self.data)
        self.assertEqual(1, len(outcome))
        outcome = await self.connection.query("SELECT * FROM user;")
        print(outcome)
        await self.connection.query("DELETE user;")
        await self.connection.socket.close()

    async def test_update_record_id(self):
        record_id = RecordID("user","tobie")
        outcome = await self.connection.update(record_id)
        print(outcome)
        # self.assertEqual(1, len(outcome))
        outcome = await self.connection.query("SELECT * FROM user;")
        print(outcome)
        await self.connection.query("DELETE user;")
        await self.connection.socket.close()

    # async def test_update_record_id_with_data(self):
    #     record_id = RecordID("user", 1)
    #     outcome = await self.connection.create(record_id, self.data)
    #     self.assertEqual("user", outcome["id"].table_name)
    #     self.assertEqual(1, outcome["id"].id)
    #     self.assertEqual(self.password, outcome["password"])
    #     self.assertEqual(self.username, outcome["username"])
    #
    #     outcome = await self.connection.query("SELECT * FROM user;")
    #     self.assertEqual(
    #         len(outcome),
    #         1
    #     )
    #     self.assertEqual("user", outcome[0]["id"].table_name)
    #     self.assertEqual(self.password, outcome[0]["password"])
    #     self.assertEqual(self.username, outcome[0]["username"])
    #
    #     await self.connection.query("DELETE user;")
    #     await self.connection.socket.close()
    #
    # async def test_update_table(self):
    #     await self.connection.query("DELETE user;")
    #
    #     table = Table("user")
    #     outcome = await self.connection.create(table)
    #     self.assertEqual("user", outcome["id"].table_name)
    #
    #     self.assertEqual(
    #         len(await self.connection.query("SELECT * FROM user;")),
    #         1
    #     )
    #
    #     await self.connection.query("DELETE user;")
    #     await self.connection.socket.close()
    #
    # async def test_update_table_with_data(self):
    #     await self.connection.query("DELETE user;")
    #
    #     table = Table("user")
    #     outcome = await self.connection.create(table, self.data)
    #     self.assertEqual("user", outcome["id"].table_name)
    #     self.assertEqual(self.password, outcome["password"])
    #     self.assertEqual(self.username, outcome["username"])
    #
    #     outcome = await self.connection.query("SELECT * FROM user;")
    #     self.assertEqual(
    #         len(outcome),
    #         1
    #     )
    #     self.assertEqual("user", outcome[0]["id"].table_name)
    #     self.assertEqual(self.password, outcome[0]["password"])
    #     self.assertEqual(self.username, outcome[0]["username"])
    #
    #     await self.connection.query("DELETE user;")
    #     await self.connection.socket.close()




if __name__ == "__main__":
    main()
