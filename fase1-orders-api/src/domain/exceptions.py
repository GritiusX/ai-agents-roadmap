class InsufficientStockError(Exception):
    """Se lanza cuando se pide más cantidad de un producto que la que hay en stock."""

class InvalidQuantityError(Exception):
    """Se lanza cuando se pide una cantidad inválida (negativa o cero)."""

class OrderAlreadyShippedError(Exception):
    """Se lanza cuando se intenta cancelar un pedido que ya fue enviado."""

class OrderCancelledCannotBeShippedError(Exception):
    """Se lanza cuando se intenta enviar una orden ya cancelada"""

class OrderShippedCannotBeShippedAgainError(Exception):
    """Se lanza cuando se intenta enviar una orden ya enviada"""
