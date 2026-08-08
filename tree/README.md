# Tree (Binary Tree & Binary Search Tree)

## What it is

A hierarchical, non-linear structure: a root node with child nodes, each the root of its own subtree. No cycles, exactly one path from root to any node.

- **Binary tree**: each node has at most 2 children, no ordering constraint.
- **Binary search tree (BST)**: adds the invariant `left subtree < node < right subtree` at every node — this is what makes search O(h) by discarding half the remaining tree at each step, like binary search, but with O(h) insert too (unlike a sorted array's O(n) insert).

## The critical caveat: worst-case degeneration

A plain BST has **no balance guarantee**. Inserting already-sorted data (1,2,3,4,5,...) degenerates it into a straight line — effectively a linked list — making search/insert/delete O(n) instead of O(log n). This is exactly why self-balancing variants (AVL, Red-Black trees) exist: they guarantee O(log n) height regardless of insertion order. See `avl_tree/`.

## Traversals (all O(n))

In-order (left, node, right) visits BST keys in sorted ascending order. Pre-order (node, left, right) is used for serializing/copying. Post-order (left, right, node) is used for safe deletion (children freed before parent). Level-order (BFS via a queue) visits level by level.

## Complexity

| Operation | Balanced BST | Degenerate BST |
|---|---|---|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |
| Min/Max | O(log n) | O(n) |
| Traversal | O(n) | O(n) |

## When to use

Ordered data needing both fast search and fast insert/delete (arrays give fast search via binary search but O(n) insert); range queries, "k-th smallest," sorted iteration; building block for heaps, tries, B-Trees, interval/segment trees.

## When not to use

Insertion order could be sorted/adversarial and balance isn't guaranteed — use a self-balancing tree instead of a plain BST. If you just need O(1) average lookup with no ordering requirement, a hash table is simpler and faster on average.

## Industry use cases

1. **Database indexes (B-Trees/B+ Trees)** — PostgreSQL, MySQL/InnoDB, SQLite, and Oracle implement primary indexes as B+ Trees, a multi-child generalization of BSTs optimized for disk-block reads, keeping O(log n) search while supporting fast sorted range scans (`WHERE x BETWEEN a AND b`).
2. **File systems** — NTFS, ReiserFS, Btrfs (the name literally means "B-tree FS"), and XFS use B-Trees/B+Trees to index directory entries and file metadata for fast lookup by name.
3. **Compilers** — Abstract Syntax Trees (ASTs) represent parsed source code as a tree; every compiler/interpreter (CPython, V8, GCC/Clang) builds one before code generation or execution.
4. **IP routing tables** — routers use trie-like tree structures specialized on address prefixes to do longest-prefix-match lookups at line rate.
5. **UI/DOM trees** — the browser DOM is a tree; rendering engines walk it for layout/paint, and React's virtual DOM diffing operates on tree structures to compute minimal UI updates.

## File

`tree_ds.py` — `BinarySearchTree` with insert/search/delete (three-case deletion using in-order successor), min/max, height, and all four traversals. Includes a demo showing a degenerate (sorted-insert) BST's height blowing up. Run with `python tree_ds.py`.
