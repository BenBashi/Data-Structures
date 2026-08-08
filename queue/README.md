# Queue

## What it is

A FIFO (First-In, First-Out) collection: `enqueue` at the back, `dequeue` from the front.

**Common pitfall**: implementing dequeue as `list.pop(0)` is O(n) — every remaining element shifts. Avoid it.

- **Circular buffer (ring buffer)**: fixed-size array with `head`/`tail` indices that wrap via modulo — true O(1) enqueue/dequeue, no shifting, no unbounded growth.
- **Linked-list queue**: head+tail pointers, O(1) enqueue/dequeue, unbounded.
- **Deque**: O(1) push/pop at both ends; Python's `collections.deque` is the production-ready choice.
- **Priority queue**: not FIFO — items come out in priority order via a binary heap (`heapq`). insert/extract O(log n), peek O(1).

## Complexity

| Implementation | enqueue | dequeue | notes |
|---|---|---|---|
| Naive list `pop(0)` | O(1) | O(n) | avoid |
| Circular array buffer | O(1) | O(1) | fixed capacity |
| Linked list | O(1) | O(1) | unbounded, pointer overhead |
| `collections.deque` | O(1) | O(1) | both ends, production-ready |
| Priority queue (heap) | O(log n) | O(log n) | priority order, not FIFO |

## When to use

Fair FCFS processing (task scheduling, print queues); BFS / level-order traversal; producer-consumer buffering between components at different speeds; sliding-window/rate-limiting algorithms.

## When not to use

Need priority-based ordering (use a heap); need random access by index (use an array); need strict LIFO (use a stack).

## Industry use cases

1. **Message brokers & OS scheduling** — Kafka, RabbitMQ, and AWS SQS are conceptually (and often internally) FIFO queues that decouple producers from consumers at scale; simple round-robin OS schedulers use ready-queues the same way.
2. **BFS** — shortest-path in unweighted graphs, web crawler level-by-level discovery, and "friends within N degrees" social graph queries all rely on a queue to visit nodes in increasing distance order.
3. **NIC ring buffers** — network card drivers use fixed-size circular buffers to hand off packets between hardware interrupts and the OS/kernel without dynamic allocation — essential for high-throughput, low-latency networking.
4. **Priority queues in scheduling & pathfinding** — Dijkstra's algorithm, A* pathfinding (games, robotics, GPS routing), and priority-aware OS schedulers all use a binary heap to always process the next most urgent item.

## File

`queue_ds.py` — `CircularQueue`, `LinkedQueue`, `PriorityQueue` (heap-backed), plus `bfs_shortest_path()` demonstrating the queue-driven BFS pattern. Run with `python queue_ds.py`.
