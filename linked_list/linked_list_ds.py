"""
LINKED LIST (Singly & Doubly) — Full Interview Reference
============================================================

THEORY
------
A linked list is a sequence of nodes where each node stores a value plus a
pointer/reference to the next node (and, for doubly linked lists, the
previous node too). Unlike arrays, elements are NOT contiguous in memory —
each node can live anywhere on the heap, connected only by pointers.

SINGLY LINKED LIST (SLL)
--------------------------
Node = [value | next]
Traversal is one-directional (head -> tail). Cannot walk backwards without
starting over from head.

DOUBLY LINKED LIST (DLL)
--------------------------
Node = [prev | value | next]
Traversal works both directions. Costs extra pointer per node (more memory)
but enables O(1) removal of a *known* node (no need to find its predecessor)
and O(1) operations at both ends — this is why it's the backbone of
`collections.deque` and LRU caches.

CIRCULAR LINKED LIST
-----------------------
Tail's `next` points back to head (variant of either SLL or DLL). Useful for
round-robin scheduling (e.g., OS CPU time-slicing across processes) and
buffering (circular buffers).

ARRAY VS LINKED LIST — THE CORE TRADE-OFF
--------------------------------------------
| Aspect                | Array                     | Linked List                 |
|------------------------|----------------------------|-------------------------------|
| Memory layout          | Contiguous                 | Scattered (heap nodes)        |
| Random access           | O(1)                       | O(n) — must walk from head    |
| Insert/delete at head   | O(n) (shift)                | O(1)                          |
| Insert/delete at tail   | O(1) amortized               | O(1) (if tail pointer kept)   |
| Insert/delete in middle | O(n) (shift)                | O(n) to find + O(1) to link   |
| Memory overhead         | Low (just data)             | High (pointer per node)       |
| Cache locality           | Excellent                  | Poor (pointer chasing)        |
| Extra memory per elem    | None (maybe slack)          | 1 pointer (SLL) / 2 (DLL)     |

Key interview point: linked list insert/delete is only O(1) if you ALREADY
HAVE a reference to the node (or its predecessor for SLL). Finding that node
is O(n). This nuance trips people up — "linked list insertion is O(1)" is
only half true.

WHEN TO USE
------------
- Frequent insertions/deletions at the head, or at both ends (deque use case).
- You don't need random access by index.
- Building other structures: stacks, queues, adjacency lists (graphs),
  hash table chaining buckets, LRU cache (DLL + hash map).
- Size is highly unpredictable and you want to avoid array resize-copy costs.

WHEN NOT TO USE
------------------
- You need fast random access / binary search.
- Memory overhead of pointers is a concern (embedded systems, huge datasets).
- Cache-sensitive, high-performance numeric workloads (arrays win due to locality).

INDUSTRY / REAL-WORLD USE CASES
------------------------------------
1. **LRU Cache** (used in CPU caches, database buffer pools, Redis `maxmemory`
   eviction, CDN edge caches): implemented as a doubly linked list + hash map.
   The hash map gives O(1) lookup of a node; the DLL gives O(1) move-to-front
   and O(1) eviction of the tail (least recently used) — this exact pattern
   is Java's `LinkedHashMap` internals and Python's `collections.OrderedDict`.
2. **Operating system process schedulers**: run queues are often circular
   doubly linked lists (e.g., Linux CFS red-black tree aside, older O(1)
   schedulers and many round-robin schedulers use circular linked lists to
   cycle through runnable processes/tasks).
3. **Undo/redo & browser history**: doubly linked list where each node is a
   state; back/forward buttons just move the "current" pointer — O(1) either
   direction.
4. **Hash table collision chaining**: most hash table implementations
   (Java `HashMap` before treeification, Python dict's earlier designs,
   many language runtimes) resolve collisions by chaining entries in a
   linked list per bucket.
"""

from typing import Any, Iterator, Optional


class _SNode:
    __slots__ = ("value", "next")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: Optional["_SNode"] = None


class SinglyLinkedList:
    """Singly linked list with head+tail pointers for O(1) append."""

    def __init__(self) -> None:
        self._head: Optional[_SNode] = None
        self._tail: Optional[_SNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def __iter__(self) -> Iterator[Any]:
        node = self._head
        while node:
            yield node.value
            node = node.next

    def __repr__(self) -> str:
        return "SinglyLinkedList([" + " -> ".join(str(v) for v in self) + "])"

    def push_front(self, value: Any) -> None:
        """O(1)."""
        node = _SNode(value)
        node.next = self._head
        self._head = node
        if self._tail is None:
            self._tail = node
        self._size += 1

    def push_back(self, value: Any) -> None:
        """O(1) thanks to the tail pointer."""
        node = _SNode(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def pop_front(self) -> Any:
        """O(1)."""
        if self._head is None:
            raise IndexError("pop_front from empty list")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value

    def find(self, value: Any) -> bool:
        """O(n) — must walk from head; no random access."""
        node = self._head
        while node:
            if node.value == value:
                return True
            node = node.next
        return False

    def delete_value(self, value: Any) -> bool:
        """O(n): find (O(n)) + unlink (O(1)) once found."""
        prev, node = None, self._head
        while node:
            if node.value == value:
                if prev is None:
                    self._head = node.next
                else:
                    prev.next = node.next
                if node is self._tail:
                    self._tail = prev
                self._size -= 1
                return True
            prev, node = node, node.next
        return False

    def reverse(self) -> None:
        """O(n) — classic interview question: reverse a linked list in place."""
        prev = None
        node = self._head
        self._tail = self._head
        while node:
            nxt = node.next
            node.next = prev
            prev = node
            node = nxt
        self._head = prev

    def has_cycle(self) -> bool:
        """O(n) time, O(1) space — Floyd's cycle detection (tortoise & hare).
        Classic interview question even though this implementation never
        creates cycles itself."""
        slow = fast = self._head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False


class _DNode:
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.prev: Optional["_DNode"] = None
        self.next: Optional["_DNode"] = None


class DoublyLinkedList:
    """Doubly linked list — O(1) insert/delete at both ends, bidirectional walk.
    This is the pattern behind collections.deque and LRU caches."""

    def __init__(self) -> None:
        self._head: Optional[_DNode] = None
        self._tail: Optional[_DNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        node = self._head
        while node:
            yield node.value
            node = node.next

    def __reversed__(self) -> Iterator[Any]:
        node = self._tail
        while node:
            yield node.value
            node = node.prev

    def __repr__(self) -> str:
        return "DoublyLinkedList([" + " <-> ".join(str(v) for v in self) + "])"

    def push_front(self, value: Any) -> _DNode:
        node = _DNode(value)
        node.next = self._head
        if self._head:
            self._head.prev = node
        self._head = node
        if self._tail is None:
            self._tail = node
        self._size += 1
        return node

    def push_back(self, value: Any) -> _DNode:
        node = _DNode(value)
        node.prev = self._tail
        if self._tail:
            self._tail.next = node
        self._tail = node
        if self._head is None:
            self._head = node
        self._size += 1
        return node

    def remove_node(self, node: _DNode) -> None:
        """O(1) — the key advantage of DLL: no need to search for predecessor."""
        if node.prev:
            node.prev.next = node.next
        else:
            self._head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self._tail = node.prev
        node.prev = node.next = None
        self._size -= 1

    def pop_back(self) -> Any:
        if self._tail is None:
            raise IndexError("pop_back from empty list")
        value = self._tail.value
        self.remove_node(self._tail)
        return value


def _demo() -> None:
    print("=== SinglyLinkedList ===")
    sll = SinglyLinkedList()
    for v in [1, 2, 3]:
        sll.push_back(v)
    sll.push_front(0)
    print(sll)
    sll.reverse()
    print("reversed:", sll)
    sll.delete_value(2)
    print("after delete_value(2):", sll)
    print("has_cycle:", sll.has_cycle())

    print("\n=== DoublyLinkedList (LRU-style access pattern) ===")
    dll = DoublyLinkedList()
    n1 = dll.push_back("a")
    n2 = dll.push_back("b")
    n3 = dll.push_back("c")
    print(dll)
    dll.remove_node(n2)  # O(1) removal given the node reference
    print("after O(1) remove_node(b):", dll)
    print("reversed walk:", list(reversed(dll)))


if __name__ == "__main__":
    _demo()
