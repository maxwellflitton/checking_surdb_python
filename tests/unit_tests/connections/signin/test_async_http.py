# from unittest import main, IsolatedAsyncioTestCase
# from surrealdb.connections.async_http import AsyncHttpSurrealConnection
# from surrealdb.request_message.methods import RequestMethod
# from surrealdb.request_message.message import RequestMessage
#
#
# class TestAsyncHttpSurrealConnection(IsolatedAsyncioTestCase):
#     async def asyncSetUp(self):
#         self.url = "http://localhost:8000"
#         self.password = "root"
#         self.username = "root"
#         self.database_name = "test_db"
#         self.namespace = "test_ns"
#         self.vars_params = {
#             "username": self.username,
#             "password": self.password,
#             "namespace": self.namespace,
#             "database": self.database_name,
#         }
#
#     async def test_signin_root(self):
#         connection = AsyncHttpSurrealConnection(self.url)
#         outcome = await connection.signin(self.vars_params)
#         self.assertIn("token", outcome)  # Check that the response contains a token
#
#     async def test_signin_namespace(self):
#         connection = AsyncHttpSurrealConnection(self.url)
#         # Sign in as root
#         outcome = await connection.signin(**self.vars_params)
#
#         # # Set namespace and database
#         # await connection._send(
#         #     message=RequestMessage(
#         #         connection.id,
#         #         RequestMethod.POST,
#         #         namespace=self.namespace,
#         #         database=self.database_name,
#         #     )
#         # )
#         #
#         # # Sign in with namespace
#         # vars_with_namespace = {
#         #     **self.vars_params,
#         #     "namespace": self.namespace,
#         #     "database": self.database_name,
#         # }
#         # outcome = await connection.signin(**vars_with_namespace)
#         # self.assertIn("token", outcome)  # Check that the response contains a token
#
#     async def test_signin_database(self):
#         connection = AsyncHttpSurrealConnection(self.url)
#         # Add a database parameter to the sign-in details
#         vars_with_database = {
#             **self.vars_params,
#             "database": self.database_name,
#         }
#         outcome = await connection.signin(**vars_with_database)
#         self.assertIn("token", outcome)
#
#     async def test_signin_with_record_access(self):
#         connection = AsyncHttpSurrealConnection(self.url)
#         # Simulate record access setup
#         vars_with_record_access = {
#             "namespace": self.namespace,
#             "database": self.database_name,
#             "access": "user",
#             "variables": {
#                 "email": "info@surrealdb.com",
#                 "pass": "123456",
#             },
#         }
#         outcome = await connection.signin(**vars_with_record_access)
#         self.assertIn("token", outcome)  # Check that the response contains a token
#
#
# if __name__ == "__main__":
#     main()
