#!/usr/bin/env python3
"""This module provides a pagination utility for a csv file"""

import csv
from typing import List, Tuple, Dict


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Returns the indices of the given page"""
    x, y = 0, page_size
    for i in range(1, page):
        x, y = x + page_size, y + page_size
    return x, y


class Server:
    """Server class to paginate a database of popular baby names.
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

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns truncated csv data based on pagination info"""
        assert (type(page) is int and type(page_size) is int
                and page > 0 and page_size > 0)
        x, y = index_range(page, page_size)
        return self.dataset()[x:y]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """Returns a more detailed pagination info"""
        all_data = self.dataset()
        data = self.get_page(page, page_size)
        prev_page = page - 1
        next_page = page + 1
        if prev_page <= 0 or not all_data:
            prev_page = None
        if next_page * page_size > len(all_data):
            next_page = None
        total_pages = int(len(all_data) // page_size)
        remainder = len(all_data) % page_size
        if remainder:
            total_pages += 1
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': next_page,
            'prev_page': prev_page,
            'total_pages': total_pages
        }
