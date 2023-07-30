from graphene import ObjectType, Int, Schema, Field, Mutation
from object.objectmgr import ObjectMgr

obj_mgr = ObjectMgr(9)


class Query(ObjectType):
    get_object = Field(Int)

    def resolve_get_object(self, info):
        return obj_mgr.get_object()


class FreeObject(Mutation):
    class Arguments:
        obj = Int(required=True)

    success = Field(Int)

    def mutate(self, info, obj):
        try:
            obj_mgr.free_object(obj)
            return FreeObject(success=True)
        except ValueError:
            return FreeObject(success=False)


class Mutation(ObjectType):
    free_object = FreeObject.Field()


schema = Schema(query=Query, mutation=Mutation)
