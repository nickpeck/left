import json
import unittest
from unittest import TestCase
from typing import List
from io import StringIO

from left.database.readonlydbservice import ReadOnlyJSONDBService


class TestTinyDBService(TestCase):

    @staticmethod
    def _make_data(data: List):
        db_file = StringIO(json.dumps(data))
        return ReadOnlyJSONDBService(db_file)

    def test_read_can_return_all_records(self):
        db = self._make_data([{"uid": "foo"}, {"uid": "bar"}])
        records = db.read()
        assert records == [{"uid": "foo"}, {"uid": "bar"}]

    def test_can_read_records_with_matching_attribute(self):
        db = self._make_data([{"uid": 1, "bar": "foo"}, {"uid": 2, "foo": "bar"}])
        records = db.read(bar="foo")
        assert records == [{"uid": 1, "bar": "foo"}]

    def test_can_read_records_with_specific_key(self):
        db = self._make_data([{"uid": "foo"}, {"uid": "bar"}])
        records = db.read(uid="bar")
        assert records == [{"uid": "bar"}]

    def test_read_can_specify_offset(self):
        db = self._make_data([{"uid": "foo"}, {"uid": "bar"}])
        records = db.read(offset=1)
        assert records == [{"uid": "bar"}]

    def test_read_can_specify_limit(self):
        db = self._make_data([{"uid": "foo"}, {"uid": "bar"}])
        records = db.read(limit=1)
        assert records == [{"uid": "foo"}]

    def test_read_can_specify_offset_and_limit(self):
        db = self._make_data([{"uid": "foo"}, {"uid": "bar"}, {"uid": None}])
        records = db.read(offset=1, limit=1)
        assert records == [{"uid": "bar"}]

    def test_can_use_resource(self):
        db = self._make_data({
            "my_table": {
                "1": {"my_key": 1},
                "2": {"my_key": 2}
            }
        })
        resource = db.get_resource(table_name="my_table", key_name="my_key")
        assert resource.read(my_key=1) == [{"my_key": 1}]


if __name__ == '__main__':
    unittest.main()
