"""
ARRAY (Static & Dynamic) — Full Interview Reference
=====================================================

THEORY
------
An array is a contiguous block of memory that stores elements of the same
type, accessed by an integer index in O(1) via pointer arithmetic:
    address(i) = base_address + i * element_size

Two flavors:
1. Static array — fixed size, decided at allocation time (e.g., C's `int a[10]`).
2. Dynamic array — grows/shrinks automatically (Python `list`, Java `ArrayList`,
   C++ `std::vector`, JS `Array`). Under the hood it's still a static array
   that gets reallocated + copied ("amortized growth") when it runs out of room.

WHY O(1) RANDOM ACCESS
-----------------------
Because elements are contiguous and same-sized, the CPU/runtime computes the
memory address directly from the index — no traversal needed. This is the
single biggest advantage over linked structures.

DYNAMIC ARRAY GROWTH STRATEGY (amortized analysis)
----------------------------------------------------
When capacity is exceeded, a new (usually 2x, sometimes 1.5x) buffer is
allocated and all elements are copied over — an O(n) operation. But because
doubling means we only do this O(log n) times over n insertions, the
*amortized* cost per append is O(1). This is the classic "amortized doubling"
proof interviewers love to ask about:
    Total copy cost for n appends = 1+2+4+...+n ≈ 2n → O(n) total → O(1) amortized.

If you grow by a fixed amount (e.g., +10 each time) instead of multiplicatively,
amortized append cost degrades to O(n) — a common interview trap question.

CACHE LOCALITY
---------------
Arrays are the most cache-friendly data structure: contiguous memory means
sequential access triggers CPU prefetching and stays within cache lines.
This is why array-based algorithms often outperform theoretically-equivalent
linked-list algorithms in practice, despite same Big-O.

COMPLEXITY (n = number of elements)
-------------------------------------
| Operation                  | Static Array | Dynamic Array (amortized) |
|-----------------------------|-------------|----------------------------|
| Access by index              | O(1)        | O(1)                       |
| Search (unsorted)            | O(n)        | O(n)                       |
| Search (sorted, binary)      | O(log n)    | O(log n)                   |
| Insert/Delete at end          | N/A         | O(1) amortized             |
| Insert/Delete at start/middle | N/A         | O(n) — must shift elements |
| Space                        | O(n)        | O(n), but with slack (up to 2x)|

WHEN TO USE
------------
- You need fast random access by index.
- Data size is known or grows predictably.
- You iterate sequentially often (cache locality wins).
- You do more reads than structural inserts/deletes in the middle.

WHEN NOT TO USE
-----------------
- Frequent insertions/deletions at the front or middle (use a Linked List/Deque).
- Unknown, wildly fluctuating size with tight memory constraints and no
  tolerance for over-allocation slack.
- You need O(1) insertion at arbitrary positions.

INDUSTRY / REAL-WORLD USE CASES
----------------------------------
1. Python's `list`, Java's `ArrayList`, C++'s `std::vector`, JS `Array` —
   all are dynamic arrays under the hood; the default general-purpose
   sequence container in virtually every language's standard library.
2. Database systems store table pages and column-store data
   (e.g., Apache Arrow, Parquet) in contiguous arrays for SIMD-friendly,
   cache-efficient vectorized scans — the backbone of modern OLAP engines.
3. Image/video buffers and framebuffers in OS graphics stacks are raw
   contiguous arrays of pixels — required for direct memory-mapped access
   to the GPU/display hardware.
4. Hash tables use a backing array of buckets (see hash_table_ds.py) —
   arrays are literally the substrate most other data structures are built on.
"""

from typing import Any, Iterator, Optional


class DynamicArray:
    """A from-scratch dynamic array (like a simplified Python list / C++ vector).

    Demonstrates amortized O(1) append via capacity doubling, and the O(n)
    cost of insert/delete at arbitrary positions.
    """

    INITIAL_CAPACITY = 4
    GROWTH_FACTOR = 2

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        self._data: list[Optional[Any]] = [None] * self._capacity

    # -- introspection --------------------------------------------------
    def __len__(self) -> int:
        return self._size

    def capacity(self) -> int:
        return self._capacity

    def is_empty(self) -> bool:
        return self._size == 0

    def __repr__(self) -> str:
        return f"DynamicArray({[self._data[i] for i in range(self._size)]})"

    def __iter__(self) -> Iterator[Any]:
        for i in range(self._size):
            yield self._data[i]

    # -- core operations --------------------------------------------------
    def get(self, index: int) -> Any:
        """O(1) random access."""
        self._check_index(index)
        return self._data[index]

    def set(self, index: int, value: Any) -> None:
        """O(1) overwrite."""
        self._check_index(index)
        self._data[index] = value

    def append(self, value: Any) -> None:
        """Amortized O(1). Worst case O(n) when a resize is triggered."""
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index: int, value: Any) -> None:
        """O(n): must shift every element after `index` one slot to the right."""
        if index < 0 or index > self._size:
            raise IndexError("insert index out of range")
        if self._size == self._capacity:
            self._resize(self._capacity * self.GROWTH_FACTOR)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def pop(self, index: Optional[int] = None) -> Any:
        """O(1) if popping the last element, O(n) otherwise (shift left)."""
        if self._size == 0:
            raise IndexError("pop from empty array")
        if index is None:
            index = self._size - 1
        self._check_index(index)
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1
        # Shrink to save memory once usage drops to 1/4 of capacity.
        if 0 < self._size <= self._capacity // 4:
            self._resize(max(self.INITIAL_CAPACITY, self._capacity // 2))
        return value

    def linear_search(self, value: Any) -> int:
        """O(n) — unsorted search."""
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1

    def binary_search(self, value: Any) -> int:
        """O(log n) — REQUIRES the array to already be sorted ascending."""
        lo, hi = 0, self._size - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if self._data[mid] == value:
                return mid
            if self._data[mid] < value:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    # -- internals --------------------------------------------------
    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self._size:
            raise IndexError(f"index {index} out of range for size {self._size}")

    def _resize(self, new_capacity: int) -> None:
        """O(n) — allocate new backing array and copy elements over."""
        new_data: list[Optional[Any]] = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity


def _demo() -> None:
    arr = DynamicArray()
    print("Starting capacity:", arr.capacity())

    for i in range(1, 11):
        arr.append(i * 10)
        print(f"appended {i*10:>3} -> size={len(arr)}, capacity={arr.capacity()}")

    print("\nArray contents:", arr)
    print("get(3):", arr.get(3))

    arr.insert(0, 999)
    print("\nAfter insert(0, 999):", arr)

    arr.pop(0)
    print("After pop(0):", arr)

    print("\nlinear_search(50):", arr.linear_search(50))

    sorted_arr = DynamicArray()
    for v in [1, 3, 5, 7, 9, 11, 13]:
        sorted_arr.append(v)
    print("\nSorted array:", sorted_arr)
    print("binary_search(9):", sorted_arr.binary_search(9))
    print("binary_search(4):", sorted_arr.binary_search(4))


if __name__ == "__main__":
    _demo()
