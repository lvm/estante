#!/usr/bin/env python3

import copy
import unittest

from estante import Estante


class TestEstante(unittest.TestCase):
    def setUp(self):
        self.db = Estante("./test.db")
        self.db.clear()

    # @classmethod
    def tearDown(self):
        self.db.close()

    def test_insert_and_get(self):
        data = dict(id=1, tilte="first")
        item_id = self.db.insert(data)
        self.assertIsNotNone(item_id)

        item = self.db.get(item_id)
        self.assertEqual(item, (item_id, data))

    def test_batch_insert_and_filter(self):
        items = [
            dict(id=2, title="second"),
            dict(id=3, title="third"),
            dict(id=4, title="fourth"),
        ]
        item_ids = self.db.batch_insert(items)
        self.assertEqual(len(item_ids), 3)

        results = self.db.filter(title__endswith="d")
        self.assertEqual(len(results), 2)

    def test_batch_insert_and_exclude(self):
        items = [
            dict(id=2, title="second"),
            dict(id=3, title="third"),
            dict(id=4, title="fourth"),
        ]
        item_ids = self.db.batch_insert(items)
        self.assertEqual(len(item_ids), 3)

        results = self.db.exclude(title__endswith="d")
        self.assertEqual(len(results), 1)

    def test_batch_insert_and_all(self):
        items = [
            dict(id=1, title="first one"),
            dict(id=2, title="second"),
            dict(id=3, title="third"),
            dict(id=4, title="fourth"),
        ]
        self.db.batch_insert(items)

        results = self.db.all()
        self.assertEqual(len(results), 4)
