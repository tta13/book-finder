"""
Python3 program to implement MaxHeap Operation
with built-in module heapq
for String, Numbers, Objects
"""
from functools import total_ordering

@total_ordering
class Wrapper:
	def __init__(self, val):
		self.val = val

	def __lt__(self, other):
		return self.val[1] > other.val[1]

	def __eq__(self, other):
		return self.val[1] == other.val[1]