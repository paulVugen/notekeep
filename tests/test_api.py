import json
import os
import tempfile
import unittest

import app as app_module


class NotesApiTest(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp()
        os.close(fd)
        app_module.DB = self.db_path
        self.client = app_module.app.test_client()

    def tearDown(self):
        os.unlink(self.db_path)

    def test_create_and_list(self):
        r = self.client.post("/notes", json={"title": "hello"})
        self.assertEqual(r.status_code, 201)
        r = self.client.get("/notes")
        self.assertEqual(len(json.loads(r.data)), 1)

    def test_title_required(self):
        r = self.client.post("/notes", json={})
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
