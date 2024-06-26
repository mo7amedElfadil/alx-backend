#!/usr/bin/env python3
""" FIFO Cache
"""
from base_caching import BaseCaching
from collections import OrderedDict, deque


class FIFOCache(BaseCaching):
    """FIFOCache class
        Args:
            BaseCaching: Base class for caching (parent class)
        Methods:
            put: add data to the cache
            get: retrieve data from the cache
    """
    def __init__(self):
        """Constructor for FIFOCache Class
            Initialize parent class, Cache Dictionary and FIFO queue
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.fifo = deque()

    def overflow(self):
        """Determine if the cache is full and remove the first item
        """
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            discarded = self.fifo.popleft()
            del self.cache_data[discarded]
            print('DISCARD: {}'.format(discarded))

    def put(self, key, item):
        """Add data to the cache and check valid inputs
        """
        if None in [key, item]:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
        else:
            self.overflow()
            self.cache_data[key] = item
            self.fifo.append(key)

    def get(self, key):
        """Retrieve data from the cache and check valid inputs
        """
        if None in [key, self.cache_data.get(key)]:
            return None
        return self.cache_data.get(key)
