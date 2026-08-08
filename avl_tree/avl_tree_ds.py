"""
AVL TREE (Self-Balancing BST) — Full Interview Reference
===============================================================

THEORY
------
An AVL tree (Adelson-Velsky and Landis, 1962 — the FIRST self-balancing BST
ever invented) is a binary search tree that maintains an extra invariant on
top of the normal BST invariant:

    BALANCE FACTOR of every node = height(left subtree) - height(right subtree)
    must be in {-1, 0, 1} AT ALL TIMES.

If an insert or delete pushes any node's balance factor outside that range,
the tree performs ROTATIONS to restore balance immediately. This guarantees
tree height stays O(log n) no matter what order keys are inserted — fixing
the exact worst-case weakness of a plain BST (see tree_ds.py).

WHY THIS MATTERS
-------------------
A plain BST can degenerate to O(n) height with sorted-order inserts. An AVL
tree provably never lets that happen: it is proven that AVL tree height is
always <= ~1.44 * log2(n+2), so all operations stay O(log n) worst case,
not just average case. This worst-case guarantee is the entire point of AVL
(and Red-Black) trees.

THE FOUR ROTATION CASES
----------------------------
After an insert/delete, walk back up to the root updating heights/balance
factors. The first unbalanced node (balance factor +-2) triggers one of:

1. LEFT-LEFT (LL) case: balance factor +2, left child's balance factor >= 0
   -> single RIGHT rotation.
2. RIGHT-RIGHT (RR) case: balance factor -2, right child's balance factor <= 0
   -> single LEFT rotation.
3. LEFT-RIGHT (LR) case: balance factor +2, left child's balance factor < 0
   -> LEFT rotation on the left child, THEN RIGHT rotation on this node.
4. RIGHT-LEFT (RL) case: balance factor -2, right child's balance factor > 0
   -> RIGHT rotation on the right child, THEN LEFT rotation on this node.

A single rotation is O(1) (just re-links a constant number of pointers and
recomputes a constant number of heights) — the O(log n) cost of insert/delete
comes from walking down (and back up) the tree, not from the rotation itself.

AVL VS RED-BLACK TREES (both self-balancing BSTs, common interview compare)
--------------------------------------------------------------------------------
| Aspect                | AVL Tree                        | Red-Black Tree            |
|-------------------------|-------------------------------------|-------------------------------|
| Balance strictness       | Stricter (height diff <= 1)          | Looser (roughly 2x optimal)   |
| Lookup speed              | Faster (more rigidly balanced)        | Slightly slower               |
| Insert/Delete speed        | Slower (more rotations needed)         | Faster (fewer rotations)      |
| Typical use                 | Read-heavy workloads                    | Write-heavy workloads          |
| Real-world examples           | Databases needing fast lookups            | Linux kernel (CFS scheduler, epoll), Java TreeMap/TreeSet, C++ std::map |

Interview soundbite: "AVL trees are more rigidly balanced, so lookups are
faster but rotations on insert/delete are more frequent/costly; Red-Black
trees relax the balance constraint to reduce rotation overhead on writes,
which is why most general-purpose library maps (Java TreeMap, C++ std::map)
use Red-Black trees rather than AVL."

COMPLEXITY (guaranteed, not just average)
---------------------------------------------
| Operation | AVL Tree (worst case, guaranteed) |
|-----------|--------------------------------------|
| Search     | O(log n)                            |
| Insert      | O(log n)                            |
| Delete       | O(log n)                            |
| Space         | O(n)                               |

WHEN TO USE
------------
- Need guaranteed O(log n) worst-case performance, not just average
  (real-time systems, systems where adversarial/sorted input is plausible).
- Read-heavy workload where lookup speed matters more than insert/delete
  speed (stricter balancing = shorter trees = faster reads).
- Need sorted-order iteration / range queries with a WORST-CASE guarantee,
  unlike a hash table.

WHEN NOT TO USE
------------------
- Write-heavy workload where insert/delete speed matters more than lookup —
  a Red-Black tree does fewer rotations and is often preferred here.
- You don't need sorted order and average O(1) is fine — use a hash table,
  it's simpler and typically faster in practice.
- Implementation complexity is a concern — AVL/RB trees are notably more
  complex to implement correctly than a plain BST or hash table.

INDUSTRY / REAL-WORLD USE CASES
------------------------------------
1. **Database and filesystem indexes needing guaranteed worst-case lookups**:
   some in-memory databases and indexing structures use AVL trees
   specifically because they guarantee O(log n) worst case lookups, which
   matters for latency-sensitive read-heavy systems (a plain BST could
   silently degrade to O(n) under adversarial insert order).
2. **Windows NT kernel**: uses AVL trees internally (e.g., for process/
   thread scheduling structures and virtual memory area management) where
   guaranteed logarithmic worst-case bounds matter for OS-level determinism.
3. **General self-balancing BST family in language libraries**: while many
   default library maps use Red-Black trees (Java's `TreeMap`/`TreeSet`,
   C++'s `std::map`/`std::set`, the Linux kernel's CFS scheduler and
   `epoll`), understanding AVL trees is foundational to understanding ALL
   of these — they're the conceptual ancestor, and interviewers often use
   AVL as the vehicle to test whether you understand *why* self-balancing
   matters at all, before asking how Red-Black relaxes the constraint.
4. **Version control / persistent data structure research**: AVL trees'
   strict balance and simpler invariant (vs Red-Black) make them a common
   choice in academic and persistent (immutable) data structure
   implementations where the proofs of correctness are easier to reason
   about.
"""

from typing import Any, Optional


class AVLNode:
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key: Any, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.left: Optional["AVLNode"] = None
        self.right: Optional["AVLNode"] = None
        self.height = 1  # height of a new leaf is 1 (empty subtree = 0)


class AVLTree:
    """Self-balancing BST guaranteeing O(log n) worst-case search/insert/delete."""

    def __init__(self) -> None:
        self._root: Optional[AVLNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    # -- helpers --------------------------------------------------
    def _h(self, node: Optional[AVLNode]) -> int:
        return node.height if node else 0

    def _balance_factor(self, node: Optional[AVLNode]) -> int:
        return self._h(node.left) - self._h(node.right) if node else 0

    def _update_height(self, node: AVLNode) -> None:
        node.height = 1 + max(self._h(node.left), self._h(node.right))

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """O(1) single rotation. Fixes Left-Left imbalance.

              y                x
             / \\              / \\
            x   T3   -->     T1   y
           / \\                   / \\
          T1  T2                T2  T3
        """
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """O(1) single rotation. Fixes Right-Right imbalance (mirror of rotate_right)."""
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """Check this node's balance factor and apply the correct rotation
        case (LL, RR, LR, RL) if it's outside [-1, 1]. O(1)."""
        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:  # left-heavy
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)  # LR case
            return self._rotate_right(node)  # LL case

        if balance < -1:  # right-heavy
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)  # RL case
            return self._rotate_left(node)  # RR case

        return node  # already balanced

    # -- insert --------------------------------------------------
    def insert(self, key: Any, value: Any = None) -> None:
        """O(log n) guaranteed: O(log n) to walk down + O(log n) rotations on
        the way back up, each O(1)."""
        self._root = self._insert(self._root, key, value)

    def _insert(self, node: Optional[AVLNode], key: Any, value: Any) -> AVLNode:
        if node is None:
            self._size += 1
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node
        return self._rebalance(node)

    # -- search --------------------------------------------------
    def search(self, key: Any) -> Optional[Any]:
        """O(log n) guaranteed -- unlike a plain BST, this can NEVER degrade to O(n)."""
        node = self._root
        while node:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        return None

    def __contains__(self, key: Any) -> bool:
        """O(log n). Uses key presence, not value truthiness -- correct even
        when a stored value is None."""
        node = self._root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    # -- delete --------------------------------------------------
    def delete(self, key: Any) -> None:
        """O(log n) guaranteed: standard BST delete + rebalance on the way back up."""
        self._root = self._delete(self._root, key)

    def _delete(self, node: Optional[AVLNode], key: Any) -> Optional[AVLNode]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                self._size -= 1
                return node.right
            if node.right is None:
                self._size -= 1
                return node.left
            successor = node.right
            while successor.left:
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node.right = self._delete(node.right, successor.key)
        return self._rebalance(node)

    # -- introspection --------------------------------------------------
    def height(self) -> int:
        """O(1) -- unlike a plain BST, AVL tracks height incrementally per node."""
        return self._h(self._root) - 1 if self._root else -1

    def is_balanced(self) -> bool:
        """O(n) verification that the AVL invariant holds everywhere (sanity check)."""
        def check(node: Optional[AVLNode]) -> bool:
            if node is None:
                return True
            bf = self._balance_factor(node)
            return abs(bf) <= 1 and check(node.left) and check(node.right)
        return check(self._root)

    def inorder(self):
        def _walk(node):
            if node:
                yield from _walk(node.left)
                yield node.key
                yield from _walk(node.right)
        yield from _walk(self._root)

    def __repr__(self) -> str:
        return f"AVLTree(inorder={list(self.inorder())}, height={self.height()}, balanced={self.is_balanced()})"


def _demo() -> None:
    avl = AVLTree()
    # Insert in STRICTLY SORTED order -- this would make a plain BST
    # degenerate into a linked list (height n-1). AVL stays balanced.
    keys = list(range(1, 16))
    for k in keys:
        avl.insert(k, value=f"val-{k}")

    print(avl)
    ideal_height = len(keys).bit_length() - 1
    print(f"n={len(avl)}, height={avl.height()}, theoretical minimum height~={ideal_height}")
    print("This proves AVL never degenerates, unlike a plain BST with sorted inserts.\n")

    print("search(7):", avl.search(7))
    print("search(99):", avl.search(99))

    avl.delete(1)
    avl.delete(2)
    avl.delete(3)
    print("\nafter deleting 1,2,3:", avl)
    print("still balanced:", avl.is_balanced())


if __name__ == "__main__":
    _demo()
