from modules.items.types import Item


class Inventory:
    def __init__(self, items: list[Item]):
        self._items = items
        self.items = {item.id: item for item in items}

    def get(self, item_id: str) -> Item:
        return self.items[item_id]
