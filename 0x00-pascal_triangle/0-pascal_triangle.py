#!/usr/bin/python3
"""
    0-pascal_triangle.py: pascal_triangle()
"""


def pascal_triangle(n):
    """
        returns a lis of lists of integers
        Args:
            n (int): number of lists and digits
        Returns: list of lists
    """
    if n <= 0:
        return []

    triangle = [[1]]
    for i in range(1, n):
        prev_row = triangle[-1]
        curr_row = [1]
        for j in range(1, i):
            curr_row.append(prev_row[j-1] + prev_row[j])
        curr_row.append(1)
        triangle.append(curr_row)

    return triangle
