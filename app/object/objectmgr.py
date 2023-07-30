from collections import deque
from typing import Union


class ObjectMgr:
    def __init__(self, n: int):
        self.object_pool = deque(range(1, n))
        self.allocated_objects = set()
        self.freed_objects = deque()

    def get_object(self) -> Union[int, None]:
        if self.object_pool:
            obj = self.object_pool.popleft()
            self.allocated_objects.add(obj)
            return obj
        elif self.freed_objects:
            obj = self.freed_objects.popleft()
            self.allocated_objects.add(obj)
            return obj
        else:
            return None

    def free_object(self, obj) -> Union[int, None]:
        if obj in self.allocated_objects:
            self.allocated_objects.remove(obj)
            self.freed_objects.append(obj)
            return obj
        else:
            raise ValueError("Object is not currently allocated.")
