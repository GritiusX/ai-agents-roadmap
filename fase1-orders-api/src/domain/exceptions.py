class InsufficientStockError(Exception):
    """Se lanza cuando se pide más cantidad de un producto que la que hay en stock."""

class InvalidQuantityError(Exception):
    """Se lanza cuando se pide una cantidad inválida (negativa o cero)."""