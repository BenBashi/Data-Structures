"""
HASH TABLE / MAP — Full Interview Reference
=================================================

THEORY
------
A hash table (aka hash map / dictionary) stores key-value pairs and provides
average O(1) insert/lookup/delete by transforming a key into an array index
via a hash function:
    index = hash(key) % capacity

CORE COMPONENTS
------------------
1. Hash function: deterministic, fast, and spreads keys uniformly across
   buckets to minimize collisions. Python uses SipHash for strings (with a
   randomized seed per process, to prevent hash-flooding DoS attacks).
2. Backing array of "buckets" (this is literally an Array — see array_ds.py).
3. Collision resolution strategy (two keys hashing to the same index):

   a) SEPARATE CHAINING: each bucket holds a linked list (or small dynamic
      array) of all entries that hash there. Simple, handles high load
      factors gracefully, but extra pointer memory overhead.
      This is essentially "array of linked lists" -- ties together three
      data structures directly.

   b) OPEN ADDRESSING: on collision, probe for the next open slot within
      the SAME backing array (linear probing: index+1, +2, ...; quadratic
      probing; or double hashing). No extra memory for pointers, better
      cache locality, but degrades badly at high load factor and requires
      careful handling of deletions (tombstones) to not break probe chains.

LOAD FACTOR & RESIZING
--------------------------
load_factor = size / capacity
When load factor exceeds a threshold (commonly 0.7-0.75), the table
resizes (usually doubles) and REHASHES every existing entry into the new,
larger backing array. This is O(n) when it happens but amortizes to O(1)
per insertion overall -- same amortized-doubling idea as a dynamic array,
just with a rehash instead of a plain copy.

WHY AVERAGE O(1) BUT WORST CASE O(n)
------------------------------------------
If the hash function distributes keys well and load factor is kept low,
each bucket holds ~O(1) entries on average -> O(1) average lookup.
BUT if many/all keys collide into the same bucket (adversarial input, or a
poor/predictable hash function), that bucket degenerates into a linked list
of size n -> O(n) worst case. This is a REAL, exploitable vulnerability
("hash flooding" / algorithmic complexity DoS attacks) -- why languages like
Python randomize their string hash seed per process, and why Java 8+
treeifies buckets (converts a long chain into a red-black tree, O(log n))
once a bucket gets too large.

COMPLEXITY
-----------
| Operation | Average  | Worst case (bad hash/adversarial collisions) |
|-----------|----------|---------------------------------------------|
| Insert    | O(1)     | O(n)                                          |
| Lookup    | O(1)     | O(n)                                          |
| Delete    | O(1)     | O(n)                                          |
| Space     | O(n)     | O(n)                                          |

HASH TABLE VS TREE-BASED MAP (e.g., balanced BST like a Red-Black Tree/AVL)
-------------------------------------------------------------------------------
| Aspect              | Hash Table         | Balanced BST-based Map      |
|----------------------|----------------------|-------------------------------|
| Average lookup        | O(1)                 | O(log n)                     |
| Worst-case lookup      | O(n) (rare, mitigated) | O(log n) guaranteed        |
| Ordered iteration       | No (or insertion order only in some impls) | Yes, sorted   |
| Range queries (e.g. "keys between X and Y") | No, must scan all | Yes, efficient |
| Memory                | Extra for buckets/slack | Extra for tree pointers    |

WHEN TO USE
------------
- Need O(1) average lookup/insert/delete by key, and don't need sorted order.
- Deduplication, caching, counting/frequency tables, fast membership tests.
- Implementing sets, memoization, symbol tables (compilers), database indexes
  for equality lookups.

WHEN NOT TO USE
------------------
- You need sorted iteration or range queries (use a balanced BST / B-Tree).
- Worst-case guarantees matter (real-time systems, adversarial input) —
  use a tree-based map for guaranteed O(log n).
- Memory is extremely tight and load factor slack is unacceptable.

INDUSTRY / REAL-WORLD USE CASES
------------------------------------
1. **Every language's built-in dict/map**: Python `dict`, Java `HashMap`,
   JS `Object`/`Map`, Go `map`, Ruby `Hash` — the default associative
   container everywhere, used constantly for config, caching, and lookups.
2. **Database indexing**: hash indexes in databases (e.g., PostgreSQL hash
   indexes, in-memory stores like Redis which is fundamentally a giant
   distributed hash table) provide O(1) equality lookups; combined with
   B-Trees for range queries.
3. **Symbol tables in compilers/interpreters**: variable names, function
   names -> memory addresses/definitions are stored in hash tables for
   fast lookup during parsing/compilation (this is also how Python's own
   `__dict__` for object attributes and namespaces works).
4. **Content-addressable storage / deduplication**: Git uses SHA-1/SHA-256
   hashes of file content as keys to detect duplicate blobs; CDNs and
   deduplicating file systems use hash tables keyed by content hash to
   avoid storing identical data twice.
5. **Caching layers**: Memcached and Redis are essentially network-accessible
   hash tables, and in-process LRU caches pair a hash table (O(1) lookup)
   with a doubly linked list (O(1) eviction order) — see linked_list_ds.py.
"""

from typing import Any, Iterator, Optional


class _Entry:
    __slots__ = ("key", "value")

    def __init__(self, key: Any, value: Any) -> None:
        self.key = key
        self.value = value


class ChainingHashTable:
    """Hash table using separate chaining for collision resolution.
    Each bucket is a Python list acting as a small chain of entries."""

    INITIAL_CAPACITY = 8
    LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._buckets: list[list[_Entry]] = [[] for _ in range(self._capacity)]
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _hash(self, key: Any) -> int:
        """Map key -> bucket index. Python's built-in hash() already does the
        hashing (SipHash for str, randomized per process); we just mod it."""
        return hash(key) % self._capacity

    def _load_factor(self) -> float:
        return self._size / self._capacity

    def put(self, key: Any, value: Any) -> None:
        """Average O(1); worst case O(n) if the bucket chain is long."""
        if self._load_factor() >= self.LOAD_FACTOR_THRESHOLD:
            self._resize(self._capacity * 2)
        bucket = self._buckets[self._hash(key)]
        for entry in bucket:
            if entry.key == key:
                entry.value = value  # update existing
                return
        bucket.append(_Entry(key, value))
        self._size += 1

    def get(self, key: Any) -> Any:
        """Average O(1): hash to bucket, then scan the (typically short) chain."""
        bucket = self._buckets[self._hash(key)]
        for entry in bucket:
            if entry.key == key:
                return entry.value
        raise KeyError(key)

    def delete(self, key: Any) -> None:
        bucket = self._buckets[self._hash(key)]
        for i, entry in enumerate(bucket):
            if entry.key == key:
                bucket.pop(i)
                self._size -= 1
                return
        raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        bucket = self._buckets[self._hash(key)]
        return any(entry.key == key for entry in bucket)

    def _resize(self, new_capacity: int) -> None:
        """O(n): rehash every entry into a new, larger bucket array.
        Amortized O(1) per insert overall, same doubling argument as a
        dynamic array."""
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        for bucket in old_buckets:
            for entry in bucket:
                self.put(entry.key, entry.value)

    def keys(self) -> Iterator[Any]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.key

    def items(self) -> Iterator[tuple[Any, Any]]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.key, entry.value

    def bucket_distribution(self) -> list[int]:
        """Diagnostic: chain length per bucket -- useful to visualize how
        collisions cluster and why a bad hash function degrades to O(n)."""
        return [len(b) for b in self._buckets]

    def __repr__(self) -> str:
        return "ChainingHashTable({" + ", ".join(f"{k!r}: {v!r}" for k, v in self.items()) + "})"


_DELETED = object()  # tombstone marker for open addressing deletes


class OpenAddressingHashTable:
    """Hash table using linear probing for collision resolution.
    No pointer chains -- everything lives in one flat array, better cache
    locality, but needs tombstones to keep probe sequences valid after deletes."""

    INITIAL_CAPACITY = 8
    LOAD_FACTOR_THRESHOLD = 0.6  # kept lower than chaining: probing degrades faster

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._slots: list[Optional[Any]] = [None] * self._capacity
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def _load_factor(self) -> float:
        return self._size / self._capacity

    def put(self, key: Any, value: Any) -> None:
        """Average O(1); worst case O(n) under heavy clustering."""
        if self._load_factor() >= self.LOAD_FACTOR_THRESHOLD:
            self._resize(self._capacity * 2)
        idx = hash(key) % self._capacity
        first_tombstone = None
        for _ in range(self._capacity):
            slot = self._slots[idx]
            if slot is None:
                target = first_tombstone if first_tombstone is not None else idx
                self._slots[target] = _Entry(key, value)
                self._size += 1
                return
            if slot is _DELETED:
                if first_tombstone is None:
                    first_tombstone = idx
            elif slot.key == key:
                slot.value = value  # update existing
                return
            idx = (idx + 1) % self._capacity  # linear probe
        raise RuntimeError("hash table full — resize logic should prevent this")

    def get(self, key: Any) -> Any:
        idx = hash(key) % self._capacity
        for _ in range(self._capacity):
            slot = self._slots[idx]
            if slot is None:
                break  # empty slot -> key definitely not present (probe chain ended)
            if slot is not _DELETED and slot.key == key:
                return slot.value
            idx = (idx + 1) % self._capacity
        raise KeyError(key)

    def delete(self, key: Any) -> None:
        """Must leave a TOMBSTONE, not None -- otherwise later probes for
        other keys that hashed to this slot and were pushed past it would
        incorrectly stop early and report 'not found'."""
        idx = hash(key) % self._capacity
        for _ in range(self._capacity):
            slot = self._slots[idx]
            if slot is None:
                raise KeyError(key)
            if slot is not _DELETED and slot.key == key:
                self._slots[idx] = _DELETED
                self._size -= 1
                return
            idx = (idx + 1) % self._capacity
        raise KeyError(key)

    def _resize(self, new_capacity: int) -> None:
        old_slots = self._slots
        self._capacity = new_capacity
        self._slots = [None] * new_capacity
        self._size = 0
        for slot in old_slots:
            if slot is not None and slot is not _DELETED:
                self.put(slot.key, slot.value)

    def __repr__(self) -> str:
        items = [(s.key, s.value) for s in self._slots if s not in (None, _DELETED)]
        return "OpenAddressingHashTable({" + ", ".join(f"{k!r}: {v!r}" for k, v in items) + "})"


def _demo() -> None:
    print("=== ChainingHashTable ===")
    ht = ChainingHashTable()
    for i in range(20):
        ht.put(f"key{i}", i * i)
    print("size:", len(ht))
    print("get('key5'):", ht.get("key5"))
    print("bucket_distribution:", ht.bucket_distribution())
    ht.delete("key5")
    print("'key5' in ht:", "key5" in ht)

    print("\n=== OpenAddressingHashTable ===")
    oa = OpenAddressingHashTable()
    for i in range(10):
        oa.put(f"k{i}", i)
    print(oa)
    oa.delete("k3")
    oa.put("k10", 100)  # should still find correct slot despite tombstone at k3
    print("after delete(k3) + put(k10):", oa)
    print("get('k7'):", oa.get("k7"))


if __name__ == "__main__":
    _demo()
