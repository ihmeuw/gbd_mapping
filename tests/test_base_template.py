from gbd_mapping.base_template import GbdRecord


class TestGbdRecord(GbdRecord):
    __slots__ = ("name", "parent")

    def __init__(self, name, parent=None):
        super().__init__()
        self.name = name
        self.parent = parent


def test_to_dict():
    record = TestGbdRecord(name="record1")
    record2 = TestGbdRecord(name="record2", parent=record)
    record.parent = record2
    record.to_dict()
