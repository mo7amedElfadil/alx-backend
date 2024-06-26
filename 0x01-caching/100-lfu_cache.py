#!/usr/bin/env python3
""" LFU caching algorithm
"""
from basic_cache import BaseCaching
from collections import Counter, OrderedDict


class LFUCache(BaseCaching):
    """ LFU cache algorithm
        Args:
            BaseCaching: Base class for caching
        Methods:
            put: add data to the cache
            get: retrieve data from the cache
    """

    def __init__(self):
        """ Constructor for LFUCache class
            Initialize parent class and counter
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.counter = Counter()

    def over_flow(self):
        """Determine if the cache is full and remove the least used item
        """
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discard = min(self.counter, key=self.counter.get)
            self.counter.pop(discard)
            self.cache_data.pop(discard)
            print('DISCARD: {}'.format(discard))

    def put(self, key, item):
        """Add data to the cache and check valid inputs
        """
        if None in [key, item]:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.counter[key] += 1
        else:
            self.cache_data[key] = item
            self.over_flow()
            self.counter[key] = 1

    def get(self, key):
        """Retrieve data from the cache and check valid inputs
        """
        if None in [key, self.cache_data.get(key)]:
            return None
        self.counter[key] += 1
        return self.cache_data[key]
