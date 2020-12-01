# chest.py
"""Class for Chest objects"""

import time
import p_func

class Chest:
    """Class Chest for creating chests that player can store and retrieve items."""

    def __init__(self, name, items, cams, gold):
        """Initializes each attribute of the Chest."""
        self._name = name
        self._items = items
        self._cams = cams
        self._gold = gold

    @property
    def name(self):
        """return self._name value"""
        return self._name

    @name.setter
    def name(self, new_name):
        """Set self._name value"""
        self._name = new_name

    @property
    def gold(self):
        """return self._gold value"""
        return self._gold

    @gold.setter
    def gold(self, amount):
        """Set self._gold value"""
        if not (amount >= 0):
            print('Insufficient funds.')

        else:
            self._gold = amount

    @property
    def cams(self):
        """return self._gold value"""
        return self._cams

    @cams.setter
    def cams(self, amount):
        """Set self._name value"""
        if not (amount >= 0):
            print('Insufficient funds.')

        else:
            self._cams = amount

    @property
    def items(self):
        """return self._items list"""
        return self._items

    @items.setter
    def items(self, item):
        """Update the self._items list"""
        _items = item

    def __repr__(self):
        return (f"Chest(name='{self.name}', items={self.items}, gold={self.gold}, cams={self.cams})")

    def add_remove_items(self, item, a_or_r):
        """Add or remove a value from self._items list
           item should be string to be added or removed
           a_or_r should be either 'a' for add or 'r' for remove
        """
        if a_or_r == 'a':
            self.items.append(item)
            p_func.animate_strings([f'You have removed {item} from your inventory and added it to the chest.'], .05)

        elif a_or_r == 'r':
            if item not in self.items:
                print('That item is not in the chest.')

            else:
                self.items.remove(item)
                p_func.animate_strings([f'You have removed {item} from the chest and placed it in your inventory.'], .05)

        else:
            raise ValueError("Must choose 'a' for add or 'r' for remove")

    def view_contents(self):
        print(f"""{self.name} Contents--\n\n{"*************Currency*************":^30}""")
        print(f"Gold: {self._gold}\n"
            f"CAMs: {self._cams}")
        print(f'{"**************Items***************":^30}')
        for item in [item for item in self._items]:
            print(f'{item}')
        print(f'{"*" * 34}\n')

    def index_of_contents(self):
        print(f"""Chest Contents--\n\n{"*************Currency*************":^30}""")
        print(f"[g]old: {self._gold}\n"
            f"[c]ams: {self._cams}")
        print(f'{"**************Items***************":^30}')
        for index, item in zip([index for index in range(len(self._items))], 
                            [item for item in self._items]):
            print(f'{[index + 1]}: {item}')
        print(f'{"*" * 34}\n')