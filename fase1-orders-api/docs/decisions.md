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

---

## Tickets resueltos (estilo TDD)

### ORDERS-1 — No se puede crear un pedido sin stock suficiente
- **Test:** `tests/domain/test_order.py::test_no_se_puede_crear_un_pedido_sin_stock_suficiente`
- **Regla:** si `quantity > product.stock`, se lanza `InsufficientStockError`.
- **Estado:** hecho (rojo → verde).

### ORDERS-2 — Rechazar pedidos con cantidad inválida (0 o negativa)
- **Estado:** en curso.
