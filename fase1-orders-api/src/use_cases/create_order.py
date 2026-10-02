from src.domain.order import Order


class CreateOrder:
    """Crea un pedido a partir de un product_id y lo guarda."""

    def __init__(self, products, orders) -> None:
        self._products = products
        self._orders = orders

    def execute(self, product_id, quantity):
        product = self._products.get(product_id)
        order = Order.create(product, quantity)
        order_id = self._orders.save(order)
        return order_id
