from __future__ import annotations
from typing import Any, Iterator, Optional, Tuple
import timeit


class Nodo:
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional["Nodo"] = None


class ListaEnlazadaSimple:

    # Ejercicio 1
    def __init__(self, iterable=None):
        self.head: Optional[Nodo] = None
        self._size = 0

        if iterable is not None:
            for value in iterable:
                self.append(value)

    def append(self, value: Any) -> None:
        nuevo = Nodo(value)

        if self.head is None:
            self.head = nuevo
            self._size += 1
            return

        actual = self.head
        while actual.next is not None:
            actual = actual.next

        actual.next = nuevo
        self._size += 1

    def prepend(self, value: Any) -> None:
        nuevo = Nodo(value)
        nuevo.next = self.head
        self.head = nuevo
        self._size += 1

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[Any]:
        actual = self.head
        while actual is not None:
            yield actual.data
            actual = actual.next

    def __str__(self) -> str:
        return "->".join(str(x) for x in self) + "->None"

    # Ejercicio 2
    def delete_value(self, value: Any) -> bool:
        if self.head is None:
            return False

        if self.head.data == value:
            self.head = self.head.next
            self._size -= 1
            return True

        anterior = self.head
        actual = self.head.next

        while actual is not None:
            if actual.data == value:
                anterior.next = actual.next
                self._size -= 1
                return True

            anterior = actual
            actual = actual.next

        return False

    # Ejercicio 3
    def insert(self, index: int, value: Any) -> None:
        if index < 0 or index > self._size:
            raise IndexError("Índice fuera de rango")

        if index == 0:
            self.prepend(value)
            return

        if index == self._size:
            self.append(value)
            return

        nuevo = Nodo(value)
        actual = self.head

        for _ in range(index - 1):
            actual = actual.next

        nuevo.next = actual.next
        actual.next = nuevo
        self._size += 1

    # Ejercicio 4
    def search(self, value: Any) -> Tuple[bool, int]:
        actual = self.head
        indice = 0

        while actual is not None:
            if actual.data == value:
                return True, indice

            actual = actual.next
            indice += 1

        return False, -1

    def count(self, value: Any) -> int:
        total = 0
        actual = self.head

        while actual is not None:
            if actual.data == value:
                total += 1

            actual = actual.next

        return total

    # Ejercicio 5
    def reverse(self) -> None:
        prev = None
        curr = self.head

        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        self.head = prev

    # Ejercicio 6
    def sumar_dos_numeros(self, l1: "ListaEnlazadaSimple", l2: "ListaEnlazadaSimple") -> "ListaEnlazadaSimple":
        resultado = ListaEnlazadaSimple()
        p = l1.head
        q = l2.head
        carry = 0

        while p is not None or q is not None or carry != 0:
            x = p.data if p is not None else 0
            y = q.data if q is not None else 0

            suma = x + y + carry
            resultado.append(suma % 10)
            carry = suma // 10

            if p is not None:
                p = p.next

            if q is not None:
                q = q.next

        return resultado

    # Ejercicio 7
    def swap_pairs(self) -> None:
        dummy = Nodo(0)
        dummy.next = self.head
        prev = dummy

        while prev.next is not None and prev.next.next is not None:
            first = prev.next
            second = first.next

            first.next = second.next
            second.next = first
            prev.next = second

            prev = first

        self.head = dummy.next

    # Ejercicio 8
    def _pop_front(self):
        if self.head is None:
            return None

        value = self.head.data
        self.head = self.head.next
        self._size -= 1
        return value

    # Ejercicio 9
    def has_cycle(self) -> bool:
        slow = self.head
        fast = self.head

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

            if slow is fast:
                return True

        return False

    # Ejercicio 10
    def split_half(self) -> Tuple["ListaEnlazadaSimple", "ListaEnlazadaSimple"]:
        mitad1 = ListaEnlazadaSimple()
        mitad2 = ListaEnlazadaSimple()

        if self.head is None:
            return mitad1, mitad2

        slow = self.head
        fast = self.head

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

        actual = self.head

        while actual is not slow:
            mitad1.append(actual.data)
            actual = actual.next

        while actual is not None:
            mitad2.append(actual.data)
            actual = actual.next

        return mitad1, mitad2


class BrowserHistory:
    def __init__(self):
        self.current: Optional[str] = None
        self.back_stack = ListaEnlazadaSimple()
        self.forward_stack = ListaEnlazadaSimple()

    def visit(self, url: str) -> str:
        if self.current is not None:
            self.back_stack.prepend(self.current)

        self.current = url
        self.forward_stack = ListaEnlazadaSimple()
        return self.current

    def back(self, steps: int) -> Optional[str]:
        for _ in range(steps):
            previous = self.back_stack._pop_front()

            if previous is None:
                break

            self.forward_stack.prepend(self.current)
            self.current = previous

        return self.current

    def forward(self, steps: int) -> Optional[str]:
        for _ in range(steps):
            next_page = self.forward_stack._pop_front()

            if next_page is None:
                break

            self.back_stack.prepend(self.current)
            self.current = next_page

        return self.current


def benchmark() -> None:
    cantidad = 10_000

    tiempo_lista_python = timeit.timeit(
        stmt="""
lista = []
for i in range(cantidad):
    lista.insert(0, i)
""",
        globals={"cantidad": cantidad},
        number=1,
    )

    tiempo_lista_enlazada = timeit.timeit(
        stmt="""
lista = ListaEnlazadaSimple()
for i in range(cantidad):
    lista.prepend(i)
""",
        globals={"cantidad": cantidad, "ListaEnlazadaSimple": ListaEnlazadaSimple},
        number=1,
    )

    print("Benchmark")
    print(f"Lista Python: {tiempo_lista_python:.6f}")
    print(f"Lista enlazada: {tiempo_lista_enlazada:.6f}")


def pruebas() -> None:
    print("Ejercicio 1")
    lista1 = ListaEnlazadaSimple()
    for i in range(1, 6):
        lista1.append(i)
    lista1.prepend(0)
    print(lista1)

    print("Ejercicio 2")
    lista2 = ListaEnlazadaSimple([1, 2, 2, 3])
    lista2.delete_value(2)
    print(lista2)

    print("Ejercicio 3")
    lista3 = ListaEnlazadaSimple()
    lista3.insert(0, "a")
    lista3.insert(1, "b")
    lista3.insert(0, "z")
    print(lista3)

    print("Ejercicio 4")
    lista4 = ListaEnlazadaSimple(["fox", "quick", "brown"])
    print(lista4.search("quick"))
    print(lista4.count("fox"))

    print("Ejercicio 5")
    lista5 = ListaEnlazadaSimple([1, 2, 3])
    lista5.reverse()
    print(lista5)

    print("Ejercicio 6")
    lista6 = ListaEnlazadaSimple()
    l1 = ListaEnlazadaSimple([2, 4, 3])
    l2 = ListaEnlazadaSimple([5, 6, 4])
    print(lista6.sumar_dos_numeros(l1, l2))

    print("Ejercicio 7")
    lista7 = ListaEnlazadaSimple([1, 2, 3, 4])
    lista7.swap_pairs()
    print(lista7)

    print("Ejercicio 8")
    history = BrowserHistory()
    history.visit("a")
    history.visit("b")
    print(history.back(1))
    print(history.forward(1))

    print("Ejercicio 9")
    lista9 = ListaEnlazadaSimple([1, 2, 3])
    print(lista9.has_cycle())

    nodo1 = Nodo(1)
    nodo2 = Nodo(2)
    nodo3 = Nodo(3)
    nodo1.next = nodo2
    nodo2.next = nodo3
    nodo3.next = nodo2

    lista_ciclo = ListaEnlazadaSimple()
    lista_ciclo.head = nodo1
    lista_ciclo._size = 3
    print(lista_ciclo.has_cycle())

    print("Ejercicio 10")
    lista10 = ListaEnlazadaSimple([1, 2, 3, 4, 5])
    mitad1, mitad2 = lista10.split_half()
    print(mitad1)
    print(mitad2)

    benchmark()


if __name__ == "__main__":
    pruebas()