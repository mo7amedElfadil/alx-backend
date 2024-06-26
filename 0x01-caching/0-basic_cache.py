#!/usr/bin/env python3
"""Basic_cache module
    Simple caching system that inherits from BaseCaching
    Use the cache_data dictionary to store data
"""
from basic_cache import BaseCaching
from typing import Union


class BasicCache(BaseCaching):
    """BasicCache class
        Args:
            BaseCaching: Base class for caching (parent class)
        Methods:
            put: add data to the cache
            get: retrieve data from the cache
    """
    def put(self, key: str, item: str) -> None:
        """Add data to the cache (dictionary) and check valid inputs
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key: str) -> Union[str, None]:
        """Retrieve data from the cache (dictionary) and check valid inputs
        """
        if key and self.cache_data.get(key):
            return self.cache_data.get(key)
