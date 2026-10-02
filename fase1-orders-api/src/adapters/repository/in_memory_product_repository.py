from src.domain.product import Product


class InMemoryProductRepository:
    """Guarda productos en memoria y los devuelve por id."""

    def __init__(self):
        self._products = {}

    def save(self, product: Product) -> None:
        self._products[product.id] = product

    def get(self, product_id: int) -> Product:
        return self._products[product_id]
