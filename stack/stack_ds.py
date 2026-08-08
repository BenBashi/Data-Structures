"""
STACK — Full Interview Reference
=====================================

THEORY
------
A stack is a LIFO (Last-In, First-Out) collection: the most recently added
element is the first one removed. Core operations:
    push(x)  -> add x to the top
    pop()    -> remove and return the top element
    peek()   -> look at top without removing
    is_empty()

Can be implemented on top of EITHER a dynamic array or a linked list:
- Array-backed: push/pop at the END of the array -> O(1) amortized (same
  amortized-doubling argument as DynamicArray). Better cache locality.
- Linked-list-backed: push/pop at the HEAD -> O(1) worst case (no resize
  ever needed), but pointer overhead + poor cache locality.

Python's own `list.append` / `list.pop()` are the idiomatic array-backed
stack — this is literally what CPython recommends over `collections.deque`
for pure stack use when you don't need thread-safety, though deque is
also O(1) at both ends and is preferred when you might need queue behavior too.

WHY NOT USE `list.pop(0)` AS A STACK/QUEUE FRONT
----------------------------------------------------
`list.pop(0)` is O(n) because every remaining element must shift left one
slot. This is a very common Python interview/code-review gotcha: stacks
should always push/pop from the END of a Python list, never the front.

COMPLEXITY
-----------
| Operation | Array-backed | Linked-list-backed |
|-----------|--------------|----------------------|
| push      | O(1) amortized | O(1) worst case    |
| pop       | O(1) amortized | O(1) worst case    |
| peek      | O(1)          | O(1)                |
| search    | O(n)          | O(n)                |
| space     | O(n)          | O(n) + pointer overhead |

WHEN TO USE
------------
- You need to process things in reverse order of arrival (undo, backtracking).
- Matching / balancing problems (parentheses, HTML tags, nested expressions).
- Depth-first traversal / backtracking algorithms (explicit stack instead of
  recursion, useful to avoid recursion depth limits / stack overflow).
- Expression evaluation (infix->postfix conversion, calculator engines).

WHEN NOT TO USE
------------------
- You need access to elements other than the top (use array/deque instead).
- You need FIFO ordering (use a Queue).
- You need random access by index.

INDUSTRY / REAL-WORLD USE CASES
------------------------------------
1. **Call stack in every programming language runtime**: function calls,
   local variables, and return addresses are pushed onto a call stack;
   returning pops the frame. Stack overflow errors are literally this stack
   exceeding its allocated size — the most universal real-world stack usage.
2. **Browser back button / undo systems**: many undo implementations
   (text editors, Photoshop, IDEs) use a stack of operations/snapshots;
   undo = pop, redo = push onto a second stack.
3. **Compilers & expression parsers**: parsing balanced brackets/braces,
   converting infix to postfix (shunting-yard algorithm), and evaluating
   postfix expressions all rely on an explicit stack. The JVM and CPython
   bytecode interpreters are literally stack machines — bytecode
   instructions push/pop operands on an evaluation stack.
4. **DFS in graph algorithms**: iterative depth-first search/traversal
   (e.g., used in dependency resolution, file system walkers, and web
   crawlers) uses an explicit stack instead of relying on recursion.
"""

from typing import Any, Optional


class ArrayStack:
    """Stack backed by a Python list, pushing/popping from the END (O(1))."""

    def __init__(self) -> None:
        self._data: list[Any] = []

    def __len__(self) -> int:
        return len(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def push(self, value: Any) -> None:
        """O(1) amortized."""
        self._data.append(value)

    def pop(self) -> Any:
        """O(1) amortized."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        """O(1)."""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._data[-1]

    def __repr__(self) -> str:
        return f"ArrayStack(top -> {self._data[::-1]})"


class _SNode:
    __slots__ = ("value", "next")

    def __init__(self, value: Any, next_: Optional["_SNode"] = None) -> None:
        self.value = value
        self.next = next_


class LinkedStack:
    """Stack backed by a singly linked list; push/pop from the HEAD, O(1) worst-case."""

    def __init__(self) -> None:
        self._top: Optional[_SNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._top is None

    def push(self, value: Any) -> None:
        self._top = _SNode(value, self._top)
        self._size += 1

    def pop(self) -> Any:
        if self._top is None:
            raise IndexError("pop from empty stack")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.value

    def peek(self) -> Any:
        if self._top is None:
            raise IndexError("peek from empty stack")
        return self._top.value

    def __repr__(self) -> str:
        vals = []
        node = self._top
        while node:
            vals.append(node.value)
            node = node.next
        return f"LinkedStack(top -> {vals})"


# ---------------------------------------------------------------------------
# Classic interview applications built on top of the stack
# ---------------------------------------------------------------------------

def is_balanced(expression: str) -> bool:
    """Classic stack use case: validate matching brackets/parens/braces. O(n)."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = ArrayStack()
    for ch in expression:
        if ch in "([{":
            stack.push(ch)
        elif ch in ")]}":
            if stack.is_empty() or stack.pop() != pairs[ch]:
                return False
    return stack.is_empty()


def evaluate_postfix(tokens: list[str]) -> float:
    """Evaluate a postfix (Reverse Polish Notation) expression using a stack.
    This is exactly how stack-machine bytecode interpreters (JVM, CPython)
    evaluate expressions internally."""
    stack = ArrayStack()
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
    }
    for tok in tokens:
        if tok in ops:
            b = stack.pop()
            a = stack.pop()
            stack.push(ops[tok](a, b))
        else:
            stack.push(float(tok))
    return stack.pop()


def _demo() -> None:
    print("=== ArrayStack ===")
    s = ArrayStack()
    for v in [1, 2, 3]:
        s.push(v)
    print(s)
    print("pop:", s.pop(), "->", s)

    print("\n=== LinkedStack ===")
    ls = LinkedStack()
    for v in ["a", "b", "c"]:
        ls.push(v)
    print(ls)
    print("pop:", ls.pop(), "->", ls)

    print("\n=== is_balanced ===")
    for expr in ["({[]})", "([)]", "(()"]:
        print(f"{expr!r:10} -> {is_balanced(expr)}")

    print("\n=== evaluate_postfix ===")
    # (3 + 4) * 2  ==  postfix: 3 4 + 2 *
    print("3 4 + 2 * =", evaluate_postfix(["3", "4", "+", "2", "*"]))


if __name__ == "__main__":
    _demo()
