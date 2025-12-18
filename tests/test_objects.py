from pathlib import Path
from gait.objects import canonical_json_bytes, object_id, store_object, load_object


def test_canonical_json_stable_hash():
    a = {"b": 2, "a": 1}
    b = {"a": 1, "b": 2}
    assert canonical_json_bytes(a) == canonical_json_bytes(b)
    assert object_id(a) == object_id(b)


def test_store_and_load_object(tmp_path: Path):
    objects_dir = tmp_path / "objects"
    objects_dir.mkdir()
    obj = {"schema": "x", "n": 1}
    oid = store_object(objects_dir, obj)
    loaded = load_object(objects_dir, oid)
    assert loaded == obj
