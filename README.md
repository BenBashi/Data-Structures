# Data Structures — Interview Prep (Language-Agnostic)

Each subfolder has a from-scratch Python implementation (`*_ds.py`, runnable standalone) and a `README.md` covering theory, complexity, when (not) to use it, and real-world industry use cases.

```
array/         array_ds.py         DynamicArray
linked_list/   linked_list_ds.py   SinglyLinkedList, DoublyLinkedList
stack/         stack_ds.py         ArrayStack, LinkedStack + bracket matching, postfix eval
queue/         queue_ds.py         CircularQueue, LinkedQueue, PriorityQueue + BFS
hash_table/    hash_table_ds.py    ChainingHashTable, OpenAddressingHashTable
tree/          tree_ds.py          BinarySearchTree (unbalanced)
avl_tree/      avl_tree_ds.py      AVLTree (self-balancing)
```

Run any file directly, e.g. `python array/array_ds.py`, to see a working demo.

## Comparison table

| Structure | Access | Search | Insert | Delete | Ordered? | Space overhead |
|---|---|---|---|---|---|---|
| Array (dynamic) | O(1) | O(n) / O(log n) sorted | O(1) amortized (end), O(n) (middle) | O(n) | Insertion order | Low |
| Linked list (singly/doubly) | O(n) | O(n) | O(1) (given position) | O(1) (given node) | Insertion order | 1–2 pointers/node |
| Stack | O(1) top only | O(n) | O(1) | O(1) | LIFO | Low (array) / pointer (linked) |
| Queue | O(1) front only | O(n) | O(1) | O(1) | FIFO | Low (ring) / pointer (linked) |
| Hash table | — | O(1) avg, O(n) worst | O(1) avg, O(n) worst | O(1) avg, O(n) worst | No (or insertion order) | Bucket/slot slack |
| BST (unbalanced) | — | O(log n) avg, O(n) worst | O(log n) avg, O(n) worst | O(log n) avg, O(n) worst | Sorted | 2 pointers/node |
| AVL tree | — | O(log n) guaranteed | O(log n) guaranteed | O(log n) guaranteed | Sorted | 2 pointers + height/node |

## How to talk about "differences and when to use" in an interview

The two axes that actually matter: **how the structure lays out memory** (contiguous vs. pointer-linked vs. hashed) and **what invariant it enforces** (none, ordering, LIFO/FIFO, balance). Every trade-off falls out of those two choices.

Arrays win when you need index-based random access and can tolerate O(n) middle-inserts — contiguous memory means cache-friendly, hardware-prefetched access. Linked lists flip that trade: O(1) inserts/deletes at known positions, but O(n) to reach any position and worse cache behavior. Stacks and queues are really just "arrays or linked lists with a restricted access pattern" — the restriction (LIFO/FIFO) is the entire value, since it encodes program semantics (call stacks, scheduling) directly into the data structure. Hash tables trade ordering for average O(1) everything, by paying for it in worst-case risk and unordered iteration. Trees trade some average-case speed (vs. hash tables) for maintaining sorted order and enabling range queries — plain BSTs are the naive version, and AVL/Red-Black trees exist specifically to eliminate the plain BST's worst-case failure mode.

## Interview-ready talking points

**"When would you NOT use a hash table even though it's O(1)?"** When you need sorted iteration, range queries, or a worst-case guarantee (adversarial input can degrade a poorly-designed hash table to O(n); a balanced tree can't).

**"Why does a dynamic array's append stay O(1) if resizing is O(n)?"** Amortized analysis: doubling capacity means the total copying cost across n appends is ~2n, so it averages out to O(1) per append even though individual appends occasionally cost O(n).

**"Why do standard library maps (Java TreeMap, C++ std::map) use Red-Black trees instead of AVL?"** Red-Black trees have a looser balance constraint, so they do fewer rotations on insert/delete — better for write-heavy general-purpose use. AVL's stricter balancing makes lookups marginally faster, which favors read-heavy use cases.

**"Give 3 use cases with real internal implementations."**
- LRU cache = hash table (O(1) lookup) + doubly linked list (O(1) eviction order) — Java `LinkedHashMap`, Redis eviction, CPU/CDN caches.
- Database indexes = B+ Trees (a wide, disk-optimized BST generalization) — PostgreSQL, MySQL/InnoDB, SQLite.
- OS process scheduling / message queues = queues (FIFO) and, for priority-aware scheduling, priority queues backed by binary heaps.

## Per-structure detail

See each folder's README for full theory, the worked complexity table, when/when-not-to-use guidance, and 3+ industry use cases with specifics (product/OS/language internals).
