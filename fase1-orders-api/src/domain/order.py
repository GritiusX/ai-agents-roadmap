from __future__ import annotations

from dataclasses import dataclass

from src.domain.exceptions import InsufficientStockError
from src.domain.product import Product


@dataclass
class Order:
    product_id: int
    quantity: int

    @classmethod
    def create(cls, product: Product, quantity: int) -> Order:
        if quantity > product.stock:
            raise InsufficientStockError(
                f"No hay stock suficiente de '{product.name}': "
                f"pedido {quantity}, disponible {product.stock}"
            )

        product.stock -= quantity
        return cls(product_id=product.id, quantity=quantity)
