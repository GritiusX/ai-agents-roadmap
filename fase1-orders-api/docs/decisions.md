# Decisiones técnicas — Orders API

Registro de por qué se tomó cada decisión, no solo qué se hizo. Se va completando a medida que avanza la Fase 1.

## 1. Dominio en memoria antes que Postgres

**Decisión:** arrancar sin base de datos real, guardando todo en memoria.

**Por qué:** separar dos problemas distintos — diseñar bien las reglas de negocio (dominio) vs. persistirlas — para no pelear con Docker/Postgres y TDD al mismo tiempo. La base de datos real se suma después (tarea pendiente en `PROGRESS.md`), y el dominio no debería tener que cambiar cuando eso pase, si la arquitectura hexagonal está bien separada.

## 2. `@dataclass` en vez de clases escritas a mano

**Decisión:** `Product` y `Order` usan `@dataclass`.

**Por qué:** genera el constructor automáticamente a partir de los atributos tipados, evitando código repetitivo (`__init__` a mano). Equivalente a los "constructor promoted properties" de PHP 8.

## 3. `Order.create(...)` como factory method, no constructor directo

**Decisión:** en vez de `Order(product_id=..., quantity=...)` directo, se usa un `@classmethod create(cls, product, quantity)` que valida antes de construir.

**Por qué:** el constructor que genera `@dataclass` no tiene lugar para meter validaciones de negocio (como "no hay stock suficiente"). El patrón factory method permite validar primero y construir después, sin perder la generación automática del `__init__`.

## 4. Excepciones de dominio propias (`InsufficientStockError`)

**Decisión:** crear excepciones específicas en vez de usar `ValueError`/`Exception` genéricos.

**Por qué:** el código que llama a `Order.create(...)` (más adelante, la capa de API) necesita poder distinguir **qué** salió mal para responder distinto al usuario (ej. HTTP 409 si no hay stock, HTTP 422 si la cantidad es inválida). Con excepciones genéricas, esa distinción se pierde.

## 5. `from __future__ import annotations`

**Decisión:** agregarlo al principio de los archivos de dominio.

**Por qué:** permite que un método de `Order` devuelva `-> Order` (se referencia a sí misma) sin errores de Python, sin tener que escribir `-> "Order"` entre comillas a mano.

## 6. Estado del pedido como `Enum` (`OrderStatus`)

**Decisión:** el estado de `Order` es un `OrderStatus(Enum)` con `PENDING`, `SHIPPED` y `CANCELLED`, no un string suelto.

**Por qué:** con strings, un typo como `"shiped"` pasa sin error y el bug aparece tarde. Con un `Enum`, `OrderStatus.SHIPED` explota en el momento, y el editor autocompleta los valores válidos.

## 7. Nombres de excepciones terminan en `Error`

**Decisión:** todas las excepciones de dominio llevan el sufijo `Error` (`OrderCancelledCannotBeShippedError`, no `OrderCancelledCannotBeShipped`).

**Por qué:** es la convención de PEP 8 para excepciones, y mantiene la simetría con las que ya existían (`InsufficientStockError`, `InvalidQuantityError`, `OrderAlreadyShippedError`).

## 8. Guard clauses en las transiciones de estado

**Decisión:** `ship()` primero chequea los casos prohibidos y corta con `raise`; recién al final cambia el estado.

**Por qué:** con `if` independientes el resultado dependía del orden en que estaban escritos. Con guard clauses se lee como "si está cancelada, error; si ya fue enviada, error; si no, se envía".

## 9. Reenviar un pedido ya enviado lanza excepción (no es idempotente)

**Decisión:** `ship()` sobre un pedido `SHIPPED` lanza `OrderShippedCannotBeShippedAgainError` en vez de no hacer nada.

**Por qué:** ignorarlo en silencio era el mismo tipo de fallo silencioso que resolvió ORDERS-4, y quien llama a `ship()` dos veces probablemente tiene un bug. La alternativa (tratarlo como idempotente, porque el pedido ya está en el estado pedido) es válida y común en sistemas con reintentos; se revisa al diseñar la API REST y en la Fase 2.

---

## Tickets resueltos (estilo TDD)

### ORDERS-1 — No se puede crear un pedido sin stock suficiente
- **Test:** `tests/domain/test_order.py::test_no_se_puede_crear_un_pedido_sin_stock_suficiente`
- **Regla:** si `quantity > product.stock`, se lanza `InsufficientStockError`.
- **Estado:** hecho (rojo → verde).

### ORDERS-2 — Rechazar pedidos con cantidad inválida (0 o negativa)
- **Test:** `tests/domain/test_order.py::test_crear_un_pedido_con_cantidad_invalida_del_producto`
- **Regla:** si `quantity <= 0`, se lanza `InvalidQuantityError` (antes de chequear stock).
- **Estado:** hecho.

### ORDERS-3 — No se puede cancelar un pedido ya enviado
- **Tests:** `test_no_se_puede_cancelar_un_pedido_que_ya_fue_enviado`, `test_se_cancela_un_pedido_si_esta_pendiente_de_envio`
- **Regla:** todo `Order` nace `PENDING`; `cancel()` sobre un pedido `SHIPPED` lanza `OrderAlreadyShippedError`.
- **Estado:** hecho (rojo → verde).

### ORDERS-4 — No se puede enviar un pedido cancelado
- **Tests:** `test_no_se_envia_un_pedido_cancelado`, `test_se_envia_un_pedido_si_esta_pendiente`
- **Regla:** `ship()` sobre un pedido `CANCELLED` lanza `OrderCancelledCannotBeShippedError` y el estado no cambia.
- **Camino feliz:** se agregó un test directo de `PENDING → SHIPPED`. Ya estaba cubierto de forma indirecta por el test de ORDERS-3, pero si `ship()` se rompía, fallaba un test que habla de `cancel()` y era difícil encontrar la causa.
- **Estado:** hecho (rojo → verde).

### ORDERS-5 — No se puede reenviar un pedido ya enviado
- **Test:** `test_no_se_reenvia_un_pedido_ya_enviado`
- **Regla:** `ship()` sobre un pedido `SHIPPED` lanza `OrderShippedCannotBeShippedAgainError` y el estado no cambia. Ver decisión 9.
- **Estado:** hecho.
