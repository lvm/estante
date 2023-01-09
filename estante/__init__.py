import shelve
from typing import List, Optional
from estante.types import Item, Items, AnyValidValue
from uuid import uuid4


class Estante:
    def __init__(self, filename: str) -> None:
        self._filename: str = filename
        self._db: shelve.Shelf = shelve.open(self._filename)

    def __gen_id(self) -> str:
        return str(uuid4())

    def __filter_by_attr(
        self, items: Items, attr: str, value: str, equal: bool
    ) -> Items:
        def attr_lookup(attr, lookup, thing, value, bool_result=True):
            is_a_match: bool = False
            current_value: AnyValidValue = thing.get(attr, None)

            if not lookup:
                is_a_match = (current_value == value) == bool_result
            elif lookup == "icontains":
                is_a_match = (value.lower() in current_value.lower()) == bool_result
            elif lookup == "startswith":
                is_a_match = current_value.startswith(value) == bool_result
            elif lookup == "endswith":
                is_a_match = current_value.endswith(value) == bool_result
            elif lookup == "in":
                is_a_match = any(
                    [
                        (
                            val in current_value
                            if isinstance(current_value, list)
                            else val == current_value
                        )
                        == bool_result
                        for val in value
                    ]
                )

            return is_a_match

        matches: Items = []
        lookup: Optional[str] = None
        rel_field: Optional[str] = None
        if "__" in attr:
            attr_split: List[str] = attr.split("__")
            if len(attr_split) == 3:
                rel_field, attr, lookup = attr.split("__")
            else:
                attr, lookup = attr.split("__")

        for item_id, item in items:
            if rel_field:
                if not item.get(attr, None):
                    continue

                matches += [
                    (item_id, item)
                    for rel in item.get(rel_field, None)
                    if attr_lookup(attr, lookup, rel, value, equal)
                ]

            else:
                if not item.get(attr, None):
                    continue

                if attr_lookup(attr, lookup, item, value, equal):
                    matches.append((item_id, item))

        return matches

    def __pre_filter(self, equal: bool = True, **kwargs) -> Optional[Items]:
        if kwargs:
            results = self.all()
            if not results:
                return []

            for key, value in kwargs.items():
                results = self.__filter_by_attr(results, key, value, equal)

            return results
        return None

    def update(self, item_id: str, /, data: Item) -> None:
        return self._db.update({item_id: data})

    def insert(self, data: Item) -> str:
        item_id = self.__gen_id()
        self.update(item_id, data)
        return item_id

    def batch_insert(self, batch_data: Items) -> None:
        item_ids = []
        for data in batch_data:
            item_ids.append(self.insert(data))

        return item_ids

    def filter(self, **kwargs) -> Optional[Items]:
        return self.__pre_filter(True, **kwargs)

    def exclude(self, **kwargs) -> Optional[Items]:
        return self.__pre_filter(False, **kwargs)

    def get(self, item_id: str) -> Optional[Item]:
        return item_id, self._db.get(item_id, None)

    def all(self) -> Items:
        return list(self._db.items())

    def remove(self, item_id: str) -> None:
        self._db.pop(item_id)

    def clear(self) -> None:
        self._db.clear()

    def sync(self) -> None:
        self._db.sync()

    def close(self) -> None:
        self._db.close()
