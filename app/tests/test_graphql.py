from graphene.test import Client
from schema import schema
import pytest
from ..app import create_app
from object.objectmgr import ObjectMgr


@pytest.fixture
def my_app_context():
    test_app = create_app("TestingConfig")
    with test_app.app_context() as app_context:
        global object_mgr
        object_mgr = ObjectMgr(10)
        global client
        client = Client(schema=schema)
        yield app_context


def test_free_allocated_object(my_app_context):
    # Returns any object available in the pool. (1)
    response = client.execute(
        """
        query {
            getObject
        }
    """
    )

    # Returns the object back to the pool so that it can be given out again
    response = client.execute(
        """
        mutation {
            freeObject(obj: 1) {
                success
            }
        }
    """
    )

    assert response == {"data": {"freeObject": {"success": 1}}}


def test_free_not_allocated_object(my_app_context):
    # Request to free object that is not allocated yet

    response = client.execute(
        """
        mutation {
            freeObject(obj: 1) {
                success
            }
        }
    """
    )

    assert response == {"data": {"freeObject": {"success": 0}}}


def test_all_objects_busy(my_app_context):
    # Allocate all objects available in the pool.

    for _ in range(1, 11):
        response = client.execute(
            """
            query {
                getObject
            }
        """
        )

    # Response on empty pool.

    assert response == {"data": {"getObject": None}}


def test_free_all_busy_objects(my_app_context):
    # Free all busy objects.

    for i in range(1, 9):
        response = client.execute(
            """
            mutation {
                freeObject(obj: """
            + str(i)
            + """) {
                    success
                }
            }
        """
        )
        assert response == {"data": {"freeObject": {"success": 1}}}
    else:
        response = client.execute(
            """
            mutation {
                freeObject(obj: """
            + str(i)
            + """) {
                    success
                }
            }
        """
        )

        print("bliaaaa", i, response)
        assert response == {"data": {"freeObject": {"success": 0}}}
