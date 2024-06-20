#!/usr/bin/env python3
"""Simple Pagination
Task:
    Implement a method named get_page that takes two integer arguments page
    with default value 1 and page_size with default value 10.

    You have to use this CSV file (same as the one presented at the top of the
    project)
    Use assert to verify that both arguments are integers greater than 0.
    Use index_range to find the correct indexes to paginate the dataset
    correctly and return the appropriate page of the dataset (i.e. the correct
    list of rows).
    If the input arguments are out of range for the dataset, an empty list
    should be returned.
"""
from typing import Tuple, List
import csv


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
