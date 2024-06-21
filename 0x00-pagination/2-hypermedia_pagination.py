#!/usr/bin/env python3
"""Hypermedia pagination
Task:
    Implement a get_hyper method that takes the same arguments (and defaults)
    as get_page and returns a dictionary containing the following
    key-value pairs:
        page_size: the length of the returned dataset page
        page: the current page number
        data: the dataset page (equivalent to return from previous task)
        next_page: number of the next page, None if no next page
        prev_page: number of the previous page, None if no previous page
        total_pages: the total number of pages in the dataset as an integer

    Make sure to reuse get_page in your implementation.
    You can use the math module if necessary.
"""
from typing import Tuple, List, Union, Dict
import csv
from math import ceil


class Server:
    """Server class to paginate a database of popular baby names.
        Attributes:
            DATA_FILE : str
                The path to the CSV file containing the dataset
            __dataset : List[List]
                The dataset of popular baby names
        Methods:
            dataset() -> List[List]
                Cached dataset
            assert_inputs(page: int, page_size: int) -> None
                Assert that the inputs are integers greater than 0
            get_page(page: int = 1, page_size: int = 10) -> List[List]
                Get the page of the dataset
            index_range(page: int, page_size: int) -> Tuple[int, int]
                Provide the index range for pagination
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def assert_inputs(self, page: int, page_size: int) -> None:
        """Assert that the inputs are integers greater than 0
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Get the page of the dataset using pagination
        """
        self.assert_inputs(page, page_size)
        start, end = index_range(page, page_size)
        return self.dataset()[start:end]

    def get_hyper(self, page: int = 1,
                  page_size: int = 10) -> Dict[str,
                                               Union[int, List[List], None]]:
        """Provide the hypermedia pagination information given the page and
            page_size
        """
        data = self.get_page(page, page_size)
        rows = len(self.dataset())
        total_pages = ceil(rows / page_size)
        next_page = (None, page + 1)[page < total_pages
                                     and index_range(page,
                                                     page_size)[1] >= rows]
        prev_page = (None, page - 1)[page > 1]
        return {
                "page_size": len(data),
                "page": page,
                "data": data,
                "next_page": next_page,
                "prev_page": prev_page,
                "total_pages": total_pages
                }


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Provide the index range for pagination
        Description:
            Provide the start and end index for pagination
            The logic is:
                the start index is the page number minus 1 times the page size
                the end index is the page number times the page size
                so if page is 1 and page_size is 10, the start index is 0 and
                the end index is 10
        Parameters:
            page : int
            page_size : int
        Returns:
            Tuple[int, int]
    """
    start = (page - 1) * page_size
    end = page * page_size
    return (start, end)
