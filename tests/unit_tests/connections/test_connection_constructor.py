from unittest import TestCase, main

from surrealdb import SurrealDB, BlockingHttpSurrealConnection, BlockingWsSurrealConnection


class TestUrl(TestCase):

    def setUp(self) -> None:
        self.urls = [
            "http://localhost:5000",
            "https://localhost:5000",
            "http://localhost:5000/",
            "https://localhost:5000/",
            "ws://localhost:5000",
            "wss://localhost:5000",
            "ws://localhost:5000/",
            "wss://localhost:5000/",
        ]
        self.schemes = ["http", "https", "http", "https", "ws", "wss", "ws", "wss"]

    def test___init__(self):
        outcome = SurrealDB("ws://localhost:5000")
        self.assertEqual(type(outcome), BlockingWsSurrealConnection)

        outcome = SurrealDB("http://localhost:5000")
        self.assertEqual(type(outcome), BlockingHttpSurrealConnection)

if __name__ == "__main__":
    main()
