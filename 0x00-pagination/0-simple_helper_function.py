#!/usr/bin/env python3
"""Helper function"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Returns the indices of the given page"""
    x, y = 0, page_size
    for i in range(1, page):
        x, y = x + page_size, y + page_size
    return x, y
