#!/usr/bin/env python3
"""FIFO Cache"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """A Cache object that deletes the first added/updated when full"""

    def __init__(self):
        super().__init__()
        self.next_rank = 1
        self.cache_order = {}

    def check_overflow(self, key):
        """Delete the first item if needed"""
        if self.MAX_ITEMS != len(self.cache_data) or key in self.cache_data:
            return
        sorted_dict = dict(sorted(self.cache_order.items(),
                                  key=lambda item: item[1]))
        deleted_key = next(iter(sorted_dict))
        del self.cache_data[deleted_key]
        del self.cache_order[deleted_key]
        print("DISCARD:", deleted_key)

    def put(self, key, item):
        """Adds item to the cache"""
        if key is None or item is None:
            return
        self.check_overflow(key)
        self.cache_data[key] = item
        self.cache_order[key] = self.next_rank
        self.next_rank += 1

    def get(self, key):
        """Get an item by key"""
        if key is None:
            return
        return self.cache_data.get(key)
