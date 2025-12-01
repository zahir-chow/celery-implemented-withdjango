"""Stack implementations with short real-world stories.

Think of trays in a cafeteria or browser pages in your history: the last one
you put on the stack is the first one you will pick up again. The examples
below mirror those everyday situations to make the concept less abstract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class ListStack(Generic[T]):
    """Stack implementation powered by Python's built-in list."""

    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Cannot pop from an empty ListStack.")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("Cannot peek into an empty ListStack.")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:  # pragma: no cover - convenience only
        return f"ListStack({self._items!r})"


@dataclass
class _Node(Generic[T]):
    value: T
    next: Optional["_Node[T]"] = None


class LinkedStack(Generic[T]):
    """Stack implementation built with a singly-linked list."""

    def __init__(self) -> None:
        self._head: Optional[_Node[T]] = None
        self._size = 0




    def push(self, item: T) -> None:
        self._head = _Node(item, self._head)
        self._size += 1

    def pop(self) -> T:
        if self._head is None:
            raise IndexError("Cannot pop from an empty LinkedStack.")
        node = self._head
        self._head = node.next
        self._size -= 1
        return node.value

    def peek(self) -> T:
        if self._head is None:
            raise IndexError("Cannot peek into an empty LinkedStack.")
        return self._head.value

    def is_empty(self) -> bool:
        return self._head is None

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:  # pragma: no cover - convenience only
        values = []
        node = self._head
        while node:
            values.append(node.value)
            node = node.next
        return f"LinkedStack({values!r})"


def balance_parentheses(expression: str) -> bool:
    """Small exercise that uses a stack to verify balanced parentheses."""

    stack = ListStack[str]()
    pairs = {")": "(", "]": "[", "}": "{"}
    for char in expression:
        if char in pairs.values():
            stack.push(char)
        elif char in pairs:
            if stack.is_empty() or stack.pop() != pairs[char]:
                return False
    return stack.is_empty()


def plate_warmer_demo(order_ids: List[str]) -> List[str]:
    """Model a kitchen's stack of plates so servers always grab the newest."""

    stack = ListStack[str]()
    for order_id in order_ids:
        stack.push(order_id)

    served = []
    while not stack.is_empty():
        served.append(stack.pop())
    return served


if __name__ == "__main__":
    list_stack = ListStack[int]()
    for number in range(3):
        list_stack.push(number)
    print("ListStack pop order:", [list_stack.pop() for _ in range(len(list_stack))])

    linked_stack = LinkedStack[str]()
    for ch in ["a", "b", "c"]:
        linked_stack.push(ch)
    print("LinkedStack peek:", linked_stack.peek())

    sample = "{[()()]}"
    print(f"Is '{sample}' balanced?", balance_parentheses(sample))

    orders = ["table-1", "table-2", "table-3"]
    print("Plate warmer serving order:", plate_warmer_demo(orders))

