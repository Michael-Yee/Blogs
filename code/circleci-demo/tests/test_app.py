import json
from http import HTTPStatus
from unittest import TestCase, main
from app.app import app


class AppTestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_ping(self):

        result = self.app.get("/V1/ping")

        self.assertIsNotNone(result)
        self.assertEqual(result.status_code, HTTPStatus.OK)

        result_json = json.loads(result.data)
        self.assertEqual(result_json["ping"], "pong")


if __name__ == "__main__":
    main()