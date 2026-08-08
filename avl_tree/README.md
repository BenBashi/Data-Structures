# AVL Tree

## What it is

A self-balancing BST (Adelson-Velsky and Landis, 1962 — the first self-balancing BST ever invented). On top of the normal BST invariant, it maintains: for every node, `balance factor = height(left) - height(right)` must stay in `{-1, 0, 1}`. Any insert/delete that pushes a node's balance factor outside that range triggers a rotation to restore it immediately.

This guarantees tree height stays O(log n) — proven to be at most `~1.44 * log2(n+2)` — no matter the insertion order, fixing the exact worst-case weakness of a plain BST (see `tree/`).

## The four rotation cases

After insert/delete, walk back up updating heights; the first unbalanced node (balance factor ±2) triggers one of four cases: Left-Left → single right rotation, Right-Right → single left rotation, Left-Right → left rotation on the left child then right rotation on this node, Right-Left → right rotation on the right child then left rotation on this node. Each rotation itself is O(1); the O(log n) cost of insert/delete comes from walking the tree, not the rotation.

## AVL vs Red-Black trees

| Aspect | AVL Tree | Red-Black Tree |
|---|---|---|
| Balance strictness | Stricter (height diff ≤ 1) | Looser (~2x optimal) |
| Lookup speed | Faster | Slightly slower |
| Insert/delete speed | Slower (more rotations) | Faster (fewer rotations) |
| Typical fit | Read-heavy workloads | Write-heavy workloads |
| Examples | Databases needing fast lookups | Linux kernel (CFS scheduler, epoll), Java `TreeMap`, C++ `std::map` |

Interview soundbite: AVL trees are more rigidly balanced so lookups are faster, but rotations on insert/delete are more frequent; Red-Black trees relax the balance constraint to reduce write overhead, which is why most general-purpose library maps use Red-Black trees rather than AVL.

## Complexity (worst case, guaranteed)

| Operation | AVL Tree |
|---|---|
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |
| Space | O(n) |

## When to use

Need guaranteed O(log n) worst case, not just average (real-time systems, adversarial or sorted input is plausible); read-heavy workload where lookup speed matters most; sorted-order iteration or range queries with a worst-case guarantee, unlike a hash table.

## When not to use

Write-heavy workload where insert/delete speed matters more than lookup (Red-Black does fewer rotations); don't need sorted order and average O(1) is fine (use a hash table — simpler, typically faster); implementation complexity is a concern (AVL/RB trees are notably harder to implement correctly than a plain BST or hash table).

## Industry use cases

1. **Latency-sensitive read-heavy indexes** — some in-memory databases and indexing structures use AVL trees specifically for the guaranteed O(log n) worst-case lookup, since a plain BST could silently degrade to O(n) under adversarial insert order.
2. **Windows NT kernel** — uses AVL trees internally (e.g., for virtual memory area management and scheduling structures) where guaranteed logarithmic worst-case bounds matter for OS-level determinism.
3. **Conceptual ancestor of the self-balancing BST family** — while most library maps (Java `TreeMap`/`TreeSet`, C++ `std::map`/`std::set`, the Linux kernel's CFS scheduler and `epoll`) use Red-Black trees, AVL is the structure interviewers use to test whether you understand *why* self-balancing matters before asking how Red-Black relaxes the constraint.
4. **Persistent/immutable data structures** — AVL's stricter, simpler invariant (vs. Red-Black) makes it a common choice in academic and persistent data structure implementations where correctness proofs are easier to reason about.

## File

`avl_tree_ds.py` — `AVLTree` with insert/search/delete, all four rotation cases, incremental height tracking, and `is_balanced()` verification. Demo inserts strictly sorted keys (1..15) and shows the tree stays at near-minimum height, unlike a plain BST which would degenerate to a linked list. Run with `python avl_tree_ds.py`.
