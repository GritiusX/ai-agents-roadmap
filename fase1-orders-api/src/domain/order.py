from __future__ import annotations

from dataclasses import dataclass

from src.domain.exceptions import InsufficientStockError, InvalidQuantityError, OrderAlreadyShippedError, OrderCancelledCannotBeShippedError, OrderShippedCannotBeShippedAgainError
from src.domain.product import Product
from src.domain.enum import OrderStatus



@dataclass
class Order:
    product_id: int
    quantity: int
    status: OrderStatus = OrderStatus.PENDING

    @classmethod
    def create(cls, product: Product, quantity: int) -> Order:
        if quantity <= 0:
            raise InvalidQuantityError(
                f"La cantidad debe ser mayor que 0, se pidió {quantity}"
            )
        if quantity > product.stock:
            raise InsufficientStockError(
                f"No hay stock suficiente de '{product.name}': "
                f"pedido {quantity}, disponible {product.stock}"
            )

        product.stock -= quantity
        return cls(product_id=product.id, quantity=quantity)

    def ship(self):
        if self.status == OrderStatus.CANCELLED:
            raise OrderCancelledCannotBeShippedError(
                "No se pueden enviar ordenes ya canceladas"
            )

        if self.status == OrderStatus.SHIPPED:
            raise OrderShippedCannotBeShippedAgainError(
                "No se pueden enviar ordenes ya enviadas"
            )

        self.status = OrderStatus.SHIPPED

    def cancel(self):
        if self.status != OrderStatus.SHIPPED:
            self.status = OrderStatus.CANCELLED
        else:
            raise OrderAlreadyShippedError(
                "La orden ya fue enviada, no puede ser cancelada"
            )
