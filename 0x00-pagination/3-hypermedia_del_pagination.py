#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict, Union


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def assert_index(self, index: int) -> None:
        """Asserts if index is valid
        """
        assert index >= 0 and index < len(self.indexed_dataset())

    def get_hyper_index(self, index: Union[int, None] = None,
                        page_size: int = 10) -> Dict[str, Union[int, List]]:
        """Get the hyper index of a dataset
            The goal here is that if between two queries,
            certain rows are removed from the dataset,
            the user does not miss items from dataset when changing page.

            Method takes two arguments:
                index: index of the data to retrieve
                page_size: number of items per page
            Returns:
                dictionary with the following key-value pairs:
                    index: index of the current page
                    next_index: index of the next page
                    page_size: number of items per page
                    data: list of the data in the current page
        """
        index = index or 0
        self.assert_index(index)
        dataset = self.indexed_dataset()
        data = []
        next_index = index
        while len(data) < page_size:
            if dataset.get(next_index):
                data.append(dataset[next_index])
            next_index += 1
        return {
            "index": index,
            "next_index": next_index,
            "page_size": (page_size, len(data))[len(data) < page_size],
            "data": data
        }
