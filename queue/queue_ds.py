"""
QUEUE (FIFO, Circular, Deque, Priority Queue) — Full Interview Reference
=============================================================================

THEORY
------
A queue is a FIFO (First-In, First-Out) collection: elements are added at
the "back"/"tail" (enqueue) and removed from the "front"/"head" (dequeue).

NAIVE ARRAY IMPLEMENTATION PITFALL
-------------------------------------
If you implement a queue with a plain Python list and do
`list.pop(0)` for dequeue, that's O(n) because every remaining element
shifts left. This is the single most common queue implementation mistake.

CIRCULAR BUFFER (RING BUFFER)
---------------------------------
Fixes the above using a FIXED-size array with `head` and `tail` indices that
wrap around using modulo arithmetic:
    tail = (tail + 1) % capacity
This gives true O(1) enqueue/dequeue without shifting elements and without
unbounded growth — the standard technique for producer/consumer buffers,
audio/video streaming buffers, and OS kernel ring buffers (e.g., Linux's
`printk` log buffer, network packet ring buffers in NIC drivers).

LINKED-LIST IMPLEMENTATION
------------------------------
Using a singly linked list with head+tail pointers: enqueue at tail O(1),
dequeue at head O(1). Unbounded (grows/shrinks with the heap), unlike a
fixed-capacity ring buffer.

DEQUE (Double-Ended Queue)
------------------------------
Generalizes stack + queue: O(1) push/pop at BOTH ends. Python's
`collections.deque` is implemented as a doubly linked list of fixed-size
blocks/arrays (a hybrid) giving O(1) at both ends while avoiding some of
the pointer overhead of a pure node-per-element linked list.

PRIORITY QUEUE
-------------------
Not FIFO — elements come out in priority order, not arrival order. Typically
implemented with a binary heap (array-backed complete binary tree):
    insert: O(log n)      extract-min/max: O(log n)      peek: O(1)
Python: `heapq` module (min-heap over a list).

COMPLEXITY SUMMARY
---------------------
| Implementation      | enqueue | dequeue | notes                        |
|-----------------------|---------|---------|--------------------------------|
| Naive list (pop(0))    | O(1)    | O(n)    | AVOID for dequeue              |
| Circular array buffer   | O(1)    | O(1)    | fixed capacity                 |
| Linked list (head/tail) | O(1)    | O(1)    | unbounded, pointer overhead    |
| collections.deque       | O(1)    | O(1)    | both ends, production-ready    |
| Priority queue (heap)    | O(log n)| O(log n)| ordered by priority, not FIFO  |

WHEN TO USE
------------
- Fair, first-come-first-served processing (task scheduling, print queues).
- Breadth-first search / level-order traversal.
- Producer-consumer buffering between components running at different rates.
- Rate limiting / sliding window algorithms (deque of timestamps).

WHEN NOT TO USE
------------------
- You need priority-based ordering (use a priority queue/heap instead).
- You need random access by index (use an array).
- Strict LIFO behavior needed (use a stack).

INDUSTRY / REAL-WORLD USE CASES
------------------------------------
1. **OS process/task scheduling & message queues**: CPU ready-queues (in
   simple round-robin schedulers), and distributed message brokers like
   Kafka, RabbitMQ, and AWS SQS are conceptually (and often literally,
   internally) FIFO queues — decoupling producers and consumers at scale.
2. **BFS (Breadth-First Search)**: used in shortest-path algorithms
   (unweighted graphs), web crawlers (level-by-level page discovery),
   social network "friends within N degrees" queries — all rely on a
   queue to visit nodes level by level.
3. **Network hardware ring buffers**: NIC (network interface card) drivers
   use fixed-size circular buffers to hand off incoming packets between
   hardware interrupt handlers and the OS kernel/user-space without
   dynamic allocation overhead — critical for high-throughput low-latency
   networking.
4. **Priority queues in OS & simulation**: OS process schedulers that
   support priority levels, Dijkstra's shortest path algorithm, event-driven
   simulations, and A* pathfinding (used in games/robotics/GPS routing)
   all rely on a priority queue (binary heap) to always process the
   next most urgent/closest item first.
"""

from typing import Any, Optional
import heapq


class CircularQueue:
    """Fixed-capacity ring buffer. True O(1) enqueue/dequeue, no shifting."""

    def __init__(self, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._data: list[Optional[Any]] = [None] * capacity
        self._head = 0  # index of front element
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def is_full(self) -> bool:
        return self._size == self._capacity

    def enqueue(self, value: Any) -> None:
        """O(1). Raises if full (a real ring buffer would block/overwrite instead)."""
        if self.is_full():
            raise OverflowError("queue is full")
        tail = (self._head + self._size) % self._capacity
        self._data[tail] = value
        self._size += 1

    def dequeue(self) -> Any:
        """O(1) — no element shifting, just move the head index with wraparound."""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        value = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        return value

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._data[self._head]

    def __repr__(self) -> str:
        items = [self._data[(self._head + i) % self._capacity] for i in range(self._size)]
        return f"CircularQueue(front -> {items} <- back, cap={self._capacity})"


class _Node:
    __slots__ = ("value", "next")

    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: Optional["_Node"] = None


class LinkedQueue:
    """Unbounded queue backed by a singly linked list with head+tail pointers."""

    def __init__(self) -> None:
        self._head: Optional[_Node] = None
        self._tail: Optional[_Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def enqueue(self, value: Any) -> None:
        """O(1) — link at tail."""
        node = _Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def dequeue(self) -> Any:
        """O(1) — unlink at head."""
        if self._head is None:
            raise IndexError("dequeue from empty queue")
        node = self._head
        self._head = node.next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return node.value

    def __repr__(self) -> str:
        vals = []
        node = self._head
        while node:
            vals.append(node.value)
            node = node.next
        return f"LinkedQueue(front -> {vals} <- back)"


class PriorityQueue:
    """Min-priority queue backed by a binary heap (Python's heapq over a list).
    insert/extract are O(log n); this is NOT FIFO -- lowest priority value
    comes out first, regardless of insertion order."""

    def __init__(self) -> None:
        self._heap: list[tuple[float, int, Any]] = []
        self._counter = 0  # tie-breaker to keep heap stable & comparisons valid

    def __len__(self) -> int:
        return len(self._heap)

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def push(self, priority: float, value: Any) -> None:
        """O(log n)."""
        heapq.heappush(self._heap, (priority, self._counter, value))
        self._counter += 1

    def pop(self) -> Any:
        """O(log n) — removes and returns the lowest-priority-value item."""
        if not self._heap:
            raise IndexError("pop from empty priority queue")
        priority, _, value = heapq.heappop(self._heap)
        return value

    def peek(self) -> Any:
        """O(1)."""
        if not self._heap:
            raise IndexError("peek from empty priority queue")
        return self._heap[0][2]


def bfs_shortest_path(graph: dict[str, list[str]], start: str, goal: str) -> Optional[list[str]]:
    """Classic queue use case: BFS finds the shortest path in an unweighted
    graph because a queue guarantees nodes are visited in increasing order
    of distance from the start (level by level)."""
    from collections import deque

    frontier = deque([start])
    came_from: dict[str, Optional[str]] = {start: None}

    while frontier:
        current = frontier.popleft()  # O(1) dequeue
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return list(reversed(path))
        for neighbor in graph.get(current, []):
            if neighbor not in came_from:
                came_from[neighbor] = current
                frontier.append(neighbor)  # enqueue
    return None


def _demo() -> None:
    print("=== CircularQueue ===")
    cq = CircularQueue(3)
    cq.enqueue("a")
    cq.enqueue("b")
    cq.enqueue("c")
    print(cq)
    print("dequeue:", cq.dequeue())
    cq.enqueue("d")  # wraps around
    print("after wraparound enqueue:", cq)

    print("\n=== LinkedQueue ===")
    lq = LinkedQueue()
    for v in [1, 2, 3]:
        lq.enqueue(v)
    print(lq)
    print("dequeue:", lq.dequeue(), "->", lq)

    print("\n=== PriorityQueue (min-heap) ===")
    pq = PriorityQueue()
    pq.push(3, "medium")
    pq.push(1, "urgent")
    pq.push(5, "low")
    while not pq.is_empty():
        print("pop ->", pq.pop())

    print("\n=== BFS shortest path (queue application) ===")
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D"],
        "D": ["E"],
    }
    print("A -> E:", bfs_shortest_path(graph, "A", "E"))


if __name__ == "__main__":
    _demo()
