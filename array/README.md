# Array

## What it is

A contiguous block of memory holding same-type elements, indexed by position. `address(i) = base + i * element_size` — that arithmetic is why indexing is O(1).

- **Static array**: fixed size at allocation (C `int a[10]`).
- **Dynamic array**: resizable wrapper over a static array that reallocates + copies when full (Python `list`, Java `ArrayList`, C++ `std::vector`, JS `Array`).

## Growth strategy (the interview favorite)

Dynamic arrays double capacity when full instead of growing by a fixed amount. Doubling means the total copying cost across `n` appends is `1+2+4+...+n ≈ 2n`, so the **amortized** cost per append is O(1) even though any individual append can trigger an O(n) copy. Growing by a constant instead of a multiplier degrades amortized append to O(n) — a classic trap question.

## Complexity

| Operation | Static | Dynamic (amortized) |
|---|---|---|
| Access by index | O(1) | O(1) |
| Search (unsorted) | O(n) | O(n) |
| Search (sorted, binary) | O(log n) | O(log n) |
| Insert/delete at end | — | O(1) amortized |
| Insert/delete at start/middle | — | O(n) |
| Space | O(n) | O(n), up to 2x slack |

## When to use

Fast random access by index needed; size is known or grows predictably; sequential iteration is common (cache locality is a real, measurable win); reads dominate over middle-inserts/deletes.

## When not to use

Frequent inserts/deletes at the front or middle (prefer a linked list or deque); tight memory budget with no tolerance for allocation slack; need O(1) arbitrary-position insertion.

## Why arrays beat linked lists in practice despite equal Big-O

Contiguous memory means sequential access hits CPU cache lines and triggers hardware prefetching. A linked list with the same asymptotic complexity for traversal will still lose to an array in wall-clock time because of cache misses on every pointer hop.

## Industry use cases

1. **Standard library sequence types** — Python `list`, Java `ArrayList`, C++ `std::vector`, JS `Array` are all dynamic arrays. This is the default general-purpose container in nearly every language.
2. **Columnar analytics engines** — Apache Arrow, Parquet, and OLAP databases store column data in contiguous arrays specifically to enable SIMD vectorized scans and cache-efficient aggregation over billions of rows.
3. **Graphics/framebuffers** — OS display stacks and image buffers are raw contiguous pixel arrays, required for direct memory-mapped GPU access.
4. **Substrate for other structures** — hash tables are backed by an array of buckets; heaps are backed by an array with implicit tree indexing (`2i+1`, `2i+2`).

## File

`array_ds.py` — `DynamicArray` class implementing get/set/append/insert/pop/linear_search/binary_search from scratch, with a runnable demo (`python array_ds.py`).
