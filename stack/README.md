# Stack

## What it is

A LIFO (Last-In, First-Out) collection: `push`, `pop`, `peek`, `is_empty`. Can be backed by a dynamic array (push/pop at the end) or a linked list (push/pop at the head) — both O(1).

- **Array-backed**: better cache locality; O(1) amortized due to the same doubling strategy as a dynamic array. This is what Python's `list.append`/`list.pop()` gives you.
- **Linked-list-backed**: O(1) worst case (no resize ever), but pointer overhead and worse cache locality.

**Gotcha**: `list.pop(0)` in Python is O(n) — it shifts every remaining element. Stacks must push/pop from the *end* of a Python list, never the front.

## Complexity

| Operation | Array-backed | Linked-list-backed |
|---|---|---|
| push | O(1) amortized | O(1) worst case |
| pop | O(1) amortized | O(1) worst case |
| peek | O(1) | O(1) |
| search | O(n) | O(n) |

## When to use

Reverse-order processing (undo, backtracking); matching/balancing problems (parentheses, tags, nested expressions); DFS/backtracking with an explicit stack instead of recursion (avoids recursion-depth limits); expression evaluation (infix→postfix, calculators).

## When not to use

Need access to non-top elements; need FIFO order (use a queue); need random access by index.

## Industry use cases

1. **Function call stacks** — every language runtime pushes a frame (locals, return address) per function call and pops on return. Stack overflow errors are literally this stack exceeding its allocated size — the most universal real-world example of a stack.
2. **Undo/redo systems** — text editors, Photoshop, IDEs push operations/snapshots onto a stack; undo pops, redo pushes onto a second stack.
3. **Stack-machine bytecode interpreters** — the JVM and CPython interpreters evaluate expressions by pushing/popping operands on an evaluation stack; compilers use stacks for bracket matching and infix→postfix conversion (shunting-yard algorithm).
4. **Iterative DFS** — dependency resolution, filesystem walkers, and web crawlers often use an explicit stack for depth-first traversal instead of relying on recursion.

## File

`stack_ds.py` — `ArrayStack`, `LinkedStack`, plus classic applications `is_balanced()` (bracket matching) and `evaluate_postfix()` (RPN calculator). Run with `python stack_ds.py`.
