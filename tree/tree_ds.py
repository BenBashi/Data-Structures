"""
TREE (Binary Tree & Binary Search Tree) — Full Interview Reference
=========================================================================

THEORY
------
A tree is a hierarchical, non-linear data structure: a root node with zero
or more child nodes, each of which is itself the root of a subtree. No
cycles; exactly one path from root to any node.

Key terms: root, leaf (no children), height (longest root-to-leaf path),
depth of a node (distance from root), balanced (left/right subtree heights
differ by a bounded amount at every node).

BINARY TREE
--------------
Each node has at most 2 children (left, right). No ordering constraint.

BINARY SEARCH TREE (BST)
----------------------------
A binary tree with the BST invariant at every node:
    left subtree keys < node key < right subtree keys
This invariant is what makes search/insert/delete O(h) where h = height,
by letting you discard half the remaining tree at each step (like binary
search on a sorted array, but for a structure that supports O(h) insert
too, unlike a sorted array's O(n) insert).

CRITICAL CAVEAT — WORST CASE DEGENERATION
----------------------------------------------
A plain BST gives NO balance guarantee. Inserting already-sorted data
(1,2,3,4,5,...) degenerates the BST into a straight line — effectively a
linked list — making search/insert/delete O(n), not O(log n). This is
EXACTLY why self-balancing variants (AVL, Red-Black Trees — see
avl_tree_ds.py) exist: they guarantee O(log n) height no matter the
insertion order.

TRAVERSALS (all O(n) — must visit every node)
--------------------------------------------------
- In-order   (left, node, right)  -> visits BST keys in SORTED ascending order
- Pre-order  (node, left, right)  -> useful for copying/serializing a tree
- Post-order (left, right, node)  -> useful for safely deleting/freeing a tree
- Level-order (BFS, queue-based)  -> visits nodes level by level (see queue_ds.py)

COMPLEXITY (h = height; for a balanced tree h = O(log n), for a
degenerate/skewed tree h = O(n))
--------------------------------------------------------------------------
| Operation      | Balanced BST | Degenerate (skewed) BST |
|-----------------|--------------|----------------------------|
| Search           | O(log n)     | O(n)                       |
| Insert            | O(log n)     | O(n)                       |
| Delete            | O(log n)     | O(n)                       |
| Min/Max            | O(log n)     | O(n)                       |
| In-order traversal   | O(n)         | O(n)                       |

WHEN TO USE
------------
- Need ordered data with fast search AND fast insert/delete (arrays give
  fast search via binary search but O(n) insert; BSTs give both O(log n)
  IF balanced).
- Need range queries, "find closest", "k-th smallest", or sorted iteration.
- Building block for more advanced structures: heaps, tries, B-Trees
  (databases), interval trees, segment trees.

WHEN NOT TO USE
------------------
- Insertion order might be sorted/adversarial and you can't guarantee
  balance — use a self-balancing tree (AVL/Red-Black) instead of a plain BST.
- You just need O(1) average lookup with no ordering requirement — a hash
  table is simpler and faster on average.

INDUSTRY / REAL-WORLD USE CASES
------------------------------------
1. **Database indexes (B-Trees / B+ Trees)**: nearly every relational
   database (PostgreSQL, MySQL/InnoDB, SQLite, Oracle) implements its
   primary indexes as B+ Trees — a generalization of BSTs with many
   children per node (optimized for disk block reads) that keep O(log n)
   search while supporting fast sorted range scans (`WHERE x BETWEEN a AND b`).
2. **File systems**: many file systems (NTFS, ReiserFS, Btrfs — the name
   literally means "B-tree FS", XFS) use B-Trees/B+Trees to index
   directory entries and file metadata for fast lookup by name.
3. **Compilers**: Abstract Syntax Trees (ASTs) represent parsed source
   code as a tree — every compiler and interpreter (including CPython,
   V8, GCC/Clang) builds one during parsing before code generation/execution.
4. **Routing tables / IP lookups**: routers use trie-like tree structures
   (a variant of trees specialized on prefixes) to do longest-prefix-match
   lookups for IP routing at line rate.
5. **UI/DOM trees**: the browser DOM itself is a tree; rendering engines
   walk it for layout/paint, and diffing algorithms (React's virtual DOM)
   operate on tree structures to compute minimal UI updates.
"""

from typing import Any, Iterator, Optional
from collections import deque


class TreeNode:
    __slots__ = ("key", "value", "left", "right")

    def __init__(self, key: Any, value: Any = None) -> None:
        self.key = key
        self.value = value
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


class BinarySearchTree:
    """Unbalanced BST. O(log n) average, O(n) worst case (sorted-order inserts)."""

    def __init__(self) -> None:
        self._root: Optional[TreeNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._root is None

    # -- insert --------------------------------------------------
    def insert(self, key: Any, value: Any = None) -> None:
        """O(h). Degenerates to O(n) if inserted in sorted order (no rebalancing!)."""
        self._root = self._insert(self._root, key, value)

    def _insert(self, node: Optional[TreeNode], key: Any, value: Any) -> TreeNode:
        if node is None:
            self._size += 1
            return TreeNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value  # update existing key
        return node

    # -- search --------------------------------------------------
    def search(self, key: Any) -> Optional[Any]:
        """O(h) — discard half the remaining subtree at each step, like binary search."""
        node = self._root
        while node:
            if key == node.key:
                return node.value
            node = node.left if key < node.key else node.right
        return None

    def __contains__(self, key: Any) -> bool:
        node = self._root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    # -- delete --------------------------------------------------
    def delete(self, key: Any) -> None:
        """O(h). Three cases: leaf, one child, two children (replace with
        in-order successor -- the smallest key in the right subtree)."""
        self._root = self._delete(self._root, key)

    def _delete(self, node: Optional[TreeNode], key: Any) -> Optional[TreeNode]:
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
            # Two children: replace with in-order successor (min of right
            # subtree), then delete that successor from the right subtree.
            # Size is decremented by that recursive call, not here.
            successor = node.right
            while successor.left:
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node.right = self._delete(node.right, successor.key)
        return node

    # -- min/max --------------------------------------------------
    def find_min(self) -> Any:
        """O(h) — walk all the way left."""
        if self._root is None:
            raise ValueError("tree is empty")
        node = self._root
        while node.left:
            node = node.left
        return node.key

    def find_max(self) -> Any:
        """O(h) — walk all the way right."""
        if self._root is None:
            raise ValueError("tree is empty")
        node = self._root
        while node.right:
            node = node.right
        return node.key

    def height(self) -> int:
        """O(n) — height of empty tree is -1, single node is 0, by convention."""
        return self._height(self._root)

    def _height(self, node: Optional[TreeNode]) -> int:
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    # -- traversals (all O(n)) --------------------------------------------------
    def inorder(self) -> Iterator[Any]:
        """Visits keys in SORTED ascending order -- the defining property of a BST."""
        yield from self._inorder(self._root)

    def _inorder(self, node: Optional[TreeNode]) -> Iterator[Any]:
        if node:
            yield from self._inorder(node.left)
            yield node.key
            yield from self._inorder(node.right)

    def preorder(self) -> Iterator[Any]:
        """node, left, right -- useful for serializing/copying a tree."""
        yield from self._preorder(self._root)

    def _preorder(self, node: Optional[TreeNode]) -> Iterator[Any]:
        if node:
            yield node.key
            yield from self._preorder(node.left)
            yield from self._preorder(node.right)

    def postorder(self) -> Iterator[Any]:
        """left, right, node -- useful for safe deletion (children freed before parent)."""
        yield from self._postorder(self._root)

    def _postorder(self, node: Optional[TreeNode]) -> Iterator[Any]:
        if node:
            yield from self._postorder(node.left)
            yield from self._postorder(node.right)
            yield node.key

    def level_order(self) -> Iterator[Any]:
        """BFS traversal using a queue -- visits level by level (see queue_ds.py)."""
        if self._root is None:
            return
        q = deque([self._root])
        while q:
            node = q.popleft()
            yield node.key
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

    def __repr__(self) -> str:
        return f"BinarySearchTree(inorder={list(self.inorder())}, height={self.height()})"


def _demo() -> None:
    bst = BinarySearchTree()
    for k in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(k, value=f"val-{k}")
    print(bst)
    print("inorder (sorted):", list(bst.inorder()))
    print("preorder:", list(bst.preorder()))
    print("postorder:", list(bst.postorder()))
    print("level_order (BFS):", list(bst.level_order()))
    print("min/max:", bst.find_min(), bst.find_max())
    print("search(40):", bst.search(40))
    print("30 in bst:", 30 in bst)

    bst.delete(30)
    print("\nafter delete(30):", bst)
    print("inorder:", list(bst.inorder()))

    print("\n--- Degenerate BST demo (sorted inserts -> O(n) height) ---")
    skewed = BinarySearchTree()
    for k in range(1, 8):
        skewed.insert(k)
    print(skewed)
    print(f"height={skewed.height()} for {len(skewed)} nodes -- a balanced tree "
          f"would have height ~{(len(skewed)).bit_length() - 1}")


if __name__ == "__main__":
    _demo()
