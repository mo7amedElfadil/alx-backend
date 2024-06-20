#!/usr/bin/env python3
"""Simple helper function
Task:
    Write a function named index_range that takes two integer arguments page
    and page_size.

    The function should return a tuple of size two containing a start index
    and an end index corresponding to the range of indexes to return in a
    list for those particular pagination parameters.

    Page numbers are 1-indexed, i.e. the first page is page 1.
"""
from typing import Tuple


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
