#!/usr/bin/env python3
"""FIFO Cache"""

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """A Cache object that deletes the least frequently used item when full"""

    def __init__(self):
        super().__init__()
        self.frequency = {}
        self.usage_order = {}  # To keep track of the usage order

    def check_overflow(self, key):
        """Delete the least frequently used item if needed"""
        if self.MAX_ITEMS != len(self.cache_data) or key in self.cache_data:
            return
        min_freq = min(self.frequency.values())
        items_with_min_freq = [k for k, v in self.frequency.items() if
                               v == min_freq]
        if len(items_with_min_freq) > 1:
            # If more than one item with the lowest frequency, use
            # LRU to break the tie
            min_rank_item = min(items_with_min_freq,
                                key=lambda k: self.usage_order.get(k, 0))
            deleted_key = min_rank_item
        else:
            deleted_key = items_with_min_freq[0]

        del self.cache_data[deleted_key]
        del self.frequency[deleted_key]
        del self.usage_order[deleted_key]
        print("DISCARD:", deleted_key)

    def put(self, key, item):
        """Adds item to the cache"""
        if key is None or item is None:
            return
        self.check_overflow(key)
        self.cache_data[key] = item
        self.frequency[key] = self.frequency.get(key, 0) + 1
        self.usage_order[key] = len(self.usage_order) + 1

    def get(self, key):
        """Get an item by key"""
        if key is None or key not in self.cache_data:
            return
        self.frequency[key] = self.frequency.get(key, 0) + 1
        self.usage_order[key] = len(self.usage_order) + 1
        return self.cache_data.get(key)
