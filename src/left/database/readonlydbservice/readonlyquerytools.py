from __future__ import annotations
from typing import Dict, List, Callable


class SearchableData:
    def __init__(self, data: Dict):
        self.data = data

    def search(self, condition: Condition) -> List:
        return list(filter(lambda o: condition(o), self.data))


class Condition:
    def __init__(self, f: Callable):
        self.f = f

    def __call__(self, resource: Dict) -> bool:
        return self.f(resource)

    def __or__(self, other: Condition) -> Condition:
        def f(resource):
            return self(resource) or other(resource)
        return Condition(f)

    def __and__(self, other: Condition) -> Condition:
        def f(resource):
            return self(resource) and other(resource)
        return Condition(f)


class Where:
    def __init__(self, key):
        self.key = key

    def exists(self) -> Condition:
        def f(resource):
            return self.key in resource
        return Condition(f)

    def test(self, value) -> Condition:
        def f(resource):
            try:
                return resource[self.key] == value
            except KeyError:
                return False
        return Condition(f)
