from src.adapters.repository.in_memory_product_repository import InMemoryProductRepository
from src.domain.product import Product


def test_guardar_un_producto_y_buscarlo_por_id():
    repo = InMemoryProductRepository()
    product = Product(id=1, name="Mouse", stock=5)

    repo.save(product)

    assert repo.get(1) == product
