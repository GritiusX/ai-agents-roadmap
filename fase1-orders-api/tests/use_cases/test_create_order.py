from src.adapters.repository.in_memory_order_repository import InMemoryOrderRepository
from src.adapters.repository.in_memory_product_repository import InMemoryProductRepository
from src.domain.product import Product
from src.use_cases.create_order import CreateOrder


def test_crear_un_pedido_lo_guarda_y_descuenta_el_stock():
    orders_repo = InMemoryOrderRepository()
    products_repo = InMemoryProductRepository()

    new_product = Product(id=5, name="Mouse", stock=11)
    products_repo.save(new_product)

    create_order = CreateOrder(products=products_repo, orders=orders_repo)

    order_id = create_order.execute(product_id=5, quantity=2)

    assert orders_repo.get(order_id).quantity == 2
    assert products_repo.get(5).stock == 9
