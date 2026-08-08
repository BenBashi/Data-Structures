# Hash Table / Map

## What it is

Stores key-value pairs with average O(1) insert/lookup/delete by converting a key to an array index: `index = hash(key) % capacity`. The backing store is literally an array (see `array/`); collisions are resolved one of two ways:

- **Separate chaining**: each bucket holds a small linked list of entries that hash there. Simple, tolerates high load factors, costs pointer overhead.
- **Open addressing**: on collision, probe forward in the same array (linear/quadratic probing, double hashing). No pointer overhead, better cache locality, degrades faster at high load, and deletes require tombstones so probe chains don't break.

## Load factor and resizing

`load_factor = size / capacity`. Past a threshold (commonly 0.7–0.75), the table doubles capacity and rehashes every entry — O(n) when it happens, but amortized O(1) per insert overall, same doubling argument as a dynamic array.

## Why average O(1) but worst case O(n)

Good hash function + low load factor → ~O(1) entries per bucket → O(1) average. But if many keys collide into one bucket (adversarial input or a weak hash function), that bucket becomes an O(n) linked list. This is real and exploitable ("hash flooding" / algorithmic-complexity DoS) — why Python randomizes its string hash seed per process, and why Java 8+ treeifies long chains into a red-black tree (O(log n)) instead of leaving them as a list.

## Complexity

| Operation | Average | Worst case |
|---|---|---|
| Insert | O(1) | O(n) |
| Lookup | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Space | O(n) | O(n) |

## Hash table vs. balanced BST map

| Aspect | Hash Table | Balanced BST map (Red-Black/AVL) |
|---|---|---|
| Average lookup | O(1) | O(log n) |
| Worst-case lookup | O(n) (rare, mitigated) | O(log n) guaranteed |
| Ordered iteration | No | Yes, sorted |
| Range queries | No, must scan all | Yes, efficient |

## When to use

O(1) average lookup/insert/delete by key without needing sorted order; deduplication, caching, frequency counting, fast membership tests; sets, memoization, symbol tables, equality-based database indexes.

## When not to use

Need sorted iteration or range queries (use a balanced BST/B-Tree); need worst-case guarantees (real-time systems, adversarial input); memory is too tight to tolerate load-factor slack.

## Industry use cases

1. **Every language's built-in map** — Python `dict`, Java `HashMap`, JS `Map`/`Object`, Go `map`, Ruby `Hash`. The default associative container everywhere.
2. **Database indexing & Redis** — hash indexes give O(1) equality lookups (paired with B-Trees for range queries); Redis is fundamentally a giant network-accessible hash table.
3. **Compiler/interpreter symbol tables** — variable and function names map to definitions/addresses via a hash table during parsing and compilation; this is also how Python's own object `__dict__` and namespaces work internally.
4. **Content-addressable storage** — Git keys objects by SHA-1/SHA-256 hash of their content to detect duplicate blobs; deduplicating file systems and CDNs use the same pattern.
5. **Caching layers** — Memcached and Redis are network-accessible hash tables; in-process LRU caches pair a hash table (O(1) lookup) with a doubly linked list (O(1) eviction order).

## File

`hash_table_ds.py` — `ChainingHashTable` (separate chaining) and `OpenAddressingHashTable` (linear probing with tombstones), both with resize/rehash logic. Run with `python hash_table_ds.py`.
