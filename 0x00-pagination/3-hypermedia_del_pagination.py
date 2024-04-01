#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


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

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
    Retrieve a page of data from the dataset with deletion-resilient
    hypermedia pagination.

    Args:
        index (int, optional): The start index of the page to retrieve.
        If None, defaults to 0.
        page_size (int, optional): The number of items per page. Defaults to
        10.

    Returns:
        dict: A dictionary containing the following key-value pairs:
            - 'index': The start index of the returned page.
            - 'next_index': The index of the first item after the last item on
            the current page.
            - 'page_size': The size of the current page.
            - 'data': The actual page of the dataset.

    Raises:
        AssertionError: If the provided index is out of range
        (i.e., less than 0 or greater than the maximum index).
    """
        dataset = self.dataset()
        max_index = len(dataset) - 1

        # Check if index is within valid range
        assert index is None or 0 <= index <= max_index, "Index out of range"

        if index is None:
            index = 0

        next_index = min(index + page_size, max_index + 1)
        data = dataset[index:next_index]

        return {
            "index": index,
            "next_index": next_index,
            "page_size": page_size,
            "data": data
        }
