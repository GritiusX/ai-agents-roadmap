from src.domain.order import Order


class InMemoryOrderRepository:
    """Guarda pedidos en memoria y los devuelve por id."""

    def __init__(self):
        self._orders = {}
        self._next_id = 1

    def save(self, order: Order) -> int:
        order_id = self._next_id
        self._orders[order_id] = order
        self._next_id += 1
        return order_id

    def get(self, order_id: int) -> Order:
        return self._orders[order_id]
