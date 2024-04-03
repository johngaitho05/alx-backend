#!/usr/bin/env python3
"""Basic Cache"""

BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """Defines a basic cache"""

    def put(self, key, item):
        """Adds item to the cache"""
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Get an item by key"""
        if key is None:
            return
        return self.cache_data.get(key)
