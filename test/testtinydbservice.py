import unittest
from unittest import TestCase
from tinyrecord import transaction

from left.database.tinydbservice import TinyDBService


class TestTinyDBService(TestCase):
    DB_FILE = "test-db.json"
    DB = TinyDBService(DB_FILE)

    def setUp(self) -> None:
        with transaction(self.DB.db):
            self.DB.db.truncate()

    def test_can_create_record(self):
        self.DB.create(**{"foo": "bar"})

    def test_read_can_return_all_records(self):
        self.DB.create(**{"id": "foo"})
        self.DB.create(**{"id": "bar"})
        records = self.DB.read(keyname="id")
        assert records == [{"id": "foo"}, {"id": "bar"}]

    def test_can_read_records_with_matching_key(self):
        self.DB.create(**{"id": "foo"})
        self.DB.create(**{"bar": "foo"})
        records = self.DB.read(keyname="id")
        assert records == [{"id": "foo"}]

    def test_can_read_records_with_specific_key(self):
        self.DB.create(**{"id": "foo"})
        self.DB.create(**{"id": "bar"})
        records = self.DB.read(keyname="id", id="bar")
        assert records == [{"id": "bar"}]

    def test_read_can_specify_offset(self):
        self.DB.create(**{"id": "foo"})
        self.DB.create(**{"id": "bar"})
        records = self.DB.read(keyname="id", offset=1)
        assert records == [{"id": "bar"}]

    def test_read_can_specify_limit(self):
        self.DB.create(**{"id": "foo"})
        self.DB.create(**{"id": "bar"})
        records = self.DB.read(keyname="id", limit=1)
        assert records == [{"id": "foo"}]

    def test_read_can_specify_offset_and_limit(self):
        self.DB.create(**{"id": "foo"})
        self.DB.create(**{"id": "bar"})
        self.DB.create(**{"id": None})
        records = self.DB.read(keyname="id", offset=1, limit=1)
        assert records == [{"id": "bar"}]

    def test_can_update(self):
        self.DB.create(**{"id": "foo"})
        self.DB.create(**{"id": "bar"})
        self.DB.update(uid="foo", keyname="id", **{"id": "foo", "bar": "foo"})
        records = self.DB.read(keyname="id")
        assert records == [{"id": "foo", "bar": "foo"}, {"id": "bar"}]

    def test_can_destroy(self):
        self.DB.create(**{"id": "foo"})
        self.DB.create(**{"id": "bar"})
        self.DB.destroy(uid="foo", keyname="id")
        records = self.DB.read(keyname="id")
        assert records == [{"id": "bar"}]


if __name__ == '__main__':
    unittest.main()
