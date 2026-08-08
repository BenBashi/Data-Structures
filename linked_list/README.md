# Linked List

## What it is

A sequence of heap-allocated nodes connected by pointers instead of contiguous memory. Each node holds a value and a pointer to the next node (singly), or to both next and previous (doubly).

- **Singly linked list (SLL)**: one-directional traversal.
- **Doubly linked list (DLL)**: bidirectional; extra pointer per node, but O(1) removal given a node reference and O(1) operations at both ends.
- **Circular linked list**: tail points back to head — used for round-robin scheduling and circular buffers.

## Array vs linked list

| Aspect | Array | Linked List |
|---|---|---|
| Memory layout | Contiguous | Scattered heap nodes |
| Random access | O(1) | O(n) |
| Insert/delete at head | O(n) | O(1) |
| Insert/delete at tail | O(1) amortized | O(1) with tail pointer |
| Insert/delete in middle | O(n) shift | O(n) to find + O(1) to link |
| Cache locality | Excellent | Poor (pointer chasing) |
| Memory overhead | Low | 1–2 pointers per node |

**The nuance interviewers probe for**: linked list insert/delete is O(1) *only if you already hold a reference to the node*. Finding that node is still O(n). "Linked list insertion is O(1)" is a half-truth without that qualifier.

## When to use

Frequent inserts/deletes at the head or both ends; no need for random access by index; building blocks for other structures (stacks, queues, adjacency lists, hash table chaining, LRU caches); unpredictable size where array resize-copy is wasteful.

## When not to use

Need fast random access or binary search; memory overhead of pointers matters (embedded/huge datasets); cache-sensitive numeric workloads.

## Industry use cases

1. **LRU cache** — doubly linked list + hash map. Hash map gives O(1) node lookup; DLL gives O(1) move-to-front and O(1) tail eviction. This exact pattern underlies Java's `LinkedHashMap` and Python's `collections.OrderedDict`, and is the standard interview-favorite design for CPU/database/CDN cache eviction.
2. **OS process schedulers** — run queues are often circular (doubly) linked lists so the scheduler can cycle through runnable processes/tasks in round-robin fashion.
3. **Undo/redo, browser history** — each state is a DLL node; back/forward just moves a pointer, O(1) either direction.
4. **Hash table collision chaining** — many hash table implementations resolve collisions by chaining colliding entries in a per-bucket linked list.

## File

`linked_list_ds.py` — `SinglyLinkedList` (push_front/back, pop_front, find, delete_value, reverse, Floyd's cycle detection) and `DoublyLinkedList` (O(1) push/remove at both ends, bidirectional iteration). Run with `python linked_list_ds.py`.
