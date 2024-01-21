import unittest
from unittest import TestCase
from tinyrecord import transaction

from left.database.tinydbservice import TinyDBService, KeyNotExists


class TestTinyDBService(TestCase):
    DB_FILE = "test-db.json"
    DB_SERVICE = TinyDBService(DB_FILE)

    def setUp(self) -> None:
        with transaction(self.DB_SERVICE.db):
            self.DB_SERVICE.db.truncate()

    def test_can_create_record(self):
        self.DB_SERVICE.create(**{"uid": 1, "foo": "bar"})

    def test_read_can_return_all_records(self):
        self.DB_SERVICE.create(**{"uid": "foo"})
        self.DB_SERVICE.create(**{"uid": "bar"})
        records = self.DB_SERVICE.read()
        assert records == [{"uid": "foo"}, {"uid": "bar"}]

    def test_can_read_records_with_matching_attribute(self):
        self.DB_SERVICE.create(**{"uid": 1, "bar": "foo"})
        self.DB_SERVICE.create(**{"uid": 2, "foo": "bar"})
        records = self.DB_SERVICE.read(bar="foo")
        assert records == [{"uid": 1, "bar": "foo"}]

    def test_can_read_records_with_specific_key(self):
        self.DB_SERVICE.create(**{"uid": "foo"})
        self.DB_SERVICE.create(**{"uid": "bar"})
        records = self.DB_SERVICE.read(uid="bar")
        assert records == [{"uid": "bar"}]

    def test_read_can_specify_offset(self):
        self.DB_SERVICE.create(**{"uid": "foo"})
        self.DB_SERVICE.create(**{"uid": "bar"})
        records = self.DB_SERVICE.read(offset=1)
        assert records == [{"uid": "bar"}]

    def test_read_can_specify_limit(self):
        self.DB_SERVICE.create(**{"uid": "foo"})
        self.DB_SERVICE.create(**{"uid": "bar"})
        records = self.DB_SERVICE.read(limit=1)
        assert records == [{"uid": "foo"}]

    def test_read_can_specify_offset_and_limit(self):
        self.DB_SERVICE.create(**{"uid": "foo"})
        self.DB_SERVICE.create(**{"uid": "bar"})
        self.DB_SERVICE.create(**{"uid": None})
        records = self.DB_SERVICE.read(offset=1, limit=1)
        assert records == [{"uid": "bar"}]

    def test_can_update(self):
        self.DB_SERVICE.create(**{"uid": "foo"})
        self.DB_SERVICE.create(**{"uid": "bar"})
        self.DB_SERVICE.update(key_value="foo", **{"uid": "foo", "bar": "foo"})
        records = self.DB_SERVICE.read()
        assert records == [{"uid": "foo", "bar": "foo"}, {"uid": "bar"}]

    def test_can_destroy(self):
        self.DB_SERVICE.create(**{"uid": "foo"})
        self.DB_SERVICE.create(**{"uid": "bar"})
        self.DB_SERVICE.destroy(key_value="foo")
        records = self.DB_SERVICE.read()
        assert records == [{"uid": "bar"}]

    def test_exception_raised_if_uid_not_given(self):
        with self.assertRaises(KeyNotExists):
            self.DB_SERVICE.create(**{"id": "foo"})

    def test_can_use_resource(self):
        resource = self.DB_SERVICE.get_resource(table_name="my_table", key_name="my_key")
        record = {"my_key": 1}
        resource.create(**record)
        assert resource.read(my_key=1) == [record]
        resource.update(key_value=1, foo="bar")
        assert resource.read(my_key=1) == [{"my_key": 1, "foo": "bar"}]
        self.DB_SERVICE.create(**{"uid": 1})
        resource.destroy(key_value=1)
        assert resource.read(my_key=1) == []
        assert self.DB_SERVICE.read(uid=1) == [{"uid": 1}]


if __name__ == '__main__':
    unittest.main()
