#!/usr/bin/env python3
""" MRU Caching
"""
from basic_cache import BaseCaching
from collections import OrderedDict, deque


class MRUCache(BaseCaching):
    """MRUCache class
        Args:
            BaseCaching: Base class for caching (parent class)
        Methods:
            put: add data to the cache
            get: retrieve data from the cache
    """
    def __init__(self):
        """Initialize
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.mru = deque()

    def update_mru(self, key):
        """Update the MRU list
        """
        self.mru.remove(key)
        self.mru.append(key)

    def overflow(self):
        """Determine if the cache is full
        """
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded = self.mru.pop()
            del self.cache_data[discarded]
            print('DISCARD: {}'.format(discarded))

    def put(self, key, item):
        """Add data to the cache
        """
        if None in [key, item]:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.update_mru(key)
        else:
            self.cache_data[key] = item
            self.overflow()
            self.mru.append(key)

    def get(self, key):
        """Retrieve data from the cache
        """
        if None in [key, self.cache_data.get(key)]:
            return None
        self.update_mru(key)
        return self.cache_data.get(key)
