import pytest

from src.domain.product import Product
from src.domain.order import Order
from src.domain.exceptions import InsufficientStockError
from src.domain.exceptions import InvalidQuantityError



def test_no_se_puede_crear_un_pedido_sin_stock_suficiente():
    product = Product(id=1, name="Mouse", stock=2)

    with pytest.raises(InsufficientStockError):
        Order.create(product=product, quantity=5)


def test_crear_un_pedido_descuenta_el_stock_del_producto():
    product = Product(id=1, name="Mouse", stock=5)

    order = Order.create(product=product, quantity=2)

    assert product.stock == 3
    assert order.quantity == 2

def test_crear_un_pedido_con_stock_insuficiente_del_producto():
    product = Product(id=1, name="Mouse", stock=8)

    with pytest.raises(InvalidQuantityError):
        Order.create(product=product,quantity=-1)