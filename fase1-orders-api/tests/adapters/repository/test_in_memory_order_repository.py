from src.adapters.repository.in_memory_order_repository import InMemoryOrderRepository
from src.domain.order import Order
from src.domain.product import Product


def test_guardar_un_pedido_y_recuperarlo_por_id():
    repo = InMemoryOrderRepository()
    product = Product(id=1, name="Mouse", stock=5)
    order = Order.create(product=product, quantity=2)

    order_id = repo.save(order)

    assert repo.get(order_id) == order
