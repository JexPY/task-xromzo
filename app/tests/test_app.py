from graphene.test import Client
from schema import schema
import pytest
from ..app import create_app
from object.objectmgr import ObjectMgr


@pytest.fixture
def my_app_context():
    test_app = create_app('TestingConfig')
    with test_app.app_context() as app_context:
        global object_mgr
        object_mgr = ObjectMgr(10)
        global client
        client = Client(schema=schema)
        yield app_context

# Functionality within Flask context


def test_get_object_when_pool_is_not_empty(my_app_context):
    obj = object_mgr.get_object()
    assert obj == 1
    assert obj in object_mgr.allocated_objects


def test_get_object_when_pool_is_empty(my_app_context):
    for _ in range(1, 10):
        object_mgr.get_object()

    obj = object_mgr.get_object()
    assert obj is None


def test_free_object(my_app_context):
    obj = object_mgr.get_object()
    object_mgr.free_object(obj)
    assert obj in object_mgr.freed_objects


def test_free_object_not_currently_allocated(my_app_context):
    with pytest.raises(ValueError):
        object_mgr.free_object(100)
