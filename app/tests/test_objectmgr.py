from object.objectmgr import ObjectMgr
import pytest

object_mgr = ObjectMgr(10)


def test_get_object_when_pool_is_not_empty():
    obj = object_mgr.get_object()
    assert obj == 1
    assert obj in object_mgr.allocated_objects


def test_free_object():
    obj = object_mgr.get_object()
    object_mgr.free_object(obj)
    assert obj in object_mgr.freed_objects


def test_get_object_when_pool_is_empty():
    for _ in range(1, 10):
        object_mgr.get_object()

    obj = object_mgr.get_object()
    assert obj is None


def test_free_object_not_currently_allocated():
    with pytest.raises(ValueError):
        object_mgr.free_object(100)
