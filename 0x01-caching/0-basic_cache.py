#!/usr/bin/env python3
"""Basic_cache module
    Simple caching system that inherits from BaseCaching
    Use the cache_data dictionary to store data
"""
from basic_cache import BaseCaching


class BasicCache(BaseCaching):
    """BasicCache class
        Args:
            BaseCaching: Base class for caching (parent class)
        Methods:
            put: add data to the cache
            get: retrieve data from the cache
    """
    def put(self, key, item):
        """Add data to the cache
        """
        if None in [key, item]:
            return
        self.cache_data[key] = item

    def get(self, key):
        """Retrieve data from the cache
        """
        if None in [key, self.cache_data.get(key)]:
            return None
        return self.cache_data.get(key)
