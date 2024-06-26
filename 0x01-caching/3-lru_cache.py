#!/usr/bin/env python3
""" LRU Caching
"""
from basic_cache import BaseCaching
from collections import OrderedDict, deque


class LRUCache(BaseCaching):
    """LRUCache class
        Args:
            BaseCaching: Base class for caching (parent class)
        Methods:
            put: add data to the cache
            get: retrieve data from the cache
    """
    def __init__(self):
        super().__init__()
        self.cache_data = OrderedDict()
        self.lru = deque()

    def update_lru(self, key):
        """Update the LRU list
        """
        self.lru.remove(key)
        self.lru.append(key)

    def overflow(self):
        """Determine if the cache is full
        """
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded = self.lru.popleft()
            del self.cache_data[discarded]
            print('DISCARD: {}'.format(discarded))

    def put(self, key, item):
        """Add data to the cache
        """
        if None in [key, item]:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.update_lru(key)
        else:
            self.cache_data[key] = item
            self.overflow()
            self.lru.append(key)

    def get(self, key):
        """Retrieve data from the cache
        """
        if None in [key, self.cache_data.get(key)]:
            return None
        self.update_lru(key)
        return self.cache_data.get(key)
