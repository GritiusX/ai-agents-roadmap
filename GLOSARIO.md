# Glosario — conceptos vistos

Términos que fueron apareciendo mientras se hacía el proyecto, con **dónde** se usan en el código y un ejemplo. Complementa a [`decisions.md`](./fase1-orders-api/docs/decisions.md): allá está *por qué* se decidió algo; acá, *qué significa* cada cosa.

Rutas relativas a `fase1-orders-api/`.

---

## Testing

### TDD (rojo → verde)
Escribir el test **antes** que el código. Primero falla (rojo), después se implementa lo mínimo para que pase (verde).
- **Dónde:** todo `tests/domain/test_order.py`. El ciclo quedó visible en los commits de ORDERS-3: `4f2c930` (WIP, tests en rojo) → `53c892e` (verde).

### Rojo "feo" vs. rojo "bueno"
No todo rojo sirve.
- **Feo:** el test ni siquiera llega a correr. Ej.: `ImportError: cannot import name 'OrderCancelledCannotBeShipped'` porque la excepción todavía no existía en `exceptions.py` (o el archivo no estaba guardado). pytest dice `Interrupted: 1 error during collection`.
- **Bueno:** el test corre y falla por el motivo que querés probar. Ej.: `DID NOT RAISE OrderCancelledCannotBeShippedError` porque `ship()` todavía no lanzaba nada.
- **Cómo llegar del feo al bueno:** declarar lo que falta (la clase de excepción vacía, con su docstring) sin implementar la lógica.
- **Ojo:** el mensaje `Hint: make sure your test modules/packages have valid Python names` aparece en **cualquier** `ImportError`. Casi nunca es el problema real; leé la línea `E   ImportError: ...`.

### `pytest.raises` y el bloque `with`
`pytest.raises(X)` **no lanza** la excepción: **espera** que el código dentro del `with` la lance. Es el "juez" que mira la jugada.
- **Dónde:** `test_no_se_envia_un_pedido_cancelado`, `test_no_se_puede_cancelar_un_pedido_que_ya_fue_enviado`, etc.
```python
order.cancel()                                  # preparación: afuera
with pytest.raises(OrderCancelledCannotBeShippedError):
    order.ship()                                # SOLO la acción que debería fallar
assert order.status == OrderStatus.CANCELLED    # verificación posterior: afuera
```
- Equivale a un `try/except` que falla si no saltó la excepción (en PHPUnit: `$this->expectException(...)`).
- **Tres resultados:** salta la esperada → pasa. No salta nada → `DID NOT RAISE`. Salta otra → el test se cae con esa excepción.
- **Errores típicos:** poner la acción que falla *afuera* del `with` (explota sin que nadie la atrape) o meter *adentro* otra acción distinta (el juez mira lo que no era).

### `assert` después del `with`
Dentro del `with`, la ejecución se corta en la línea que lanza; un `assert` ahí nunca corre. Afuera, sí: sirve para verificar que el intento fallido **no dejó el objeto a medio cambiar**.
- **Dónde:** `test_no_se_envia_un_pedido_cancelado`, `test_no_se_reenvia_un_pedido_ya_enviado`.
- **Qué protege:** que alguien reordene `ship()` y cambie el estado **antes** de lanzar la excepción.

### Camino feliz (*happy path*)
El caso normal, cuando todo sale bien. Es **lo más importante** de testear: un sistema que dice "no" bien pero no hace su trabajo no sirve.
- **Dónde:** `test_crear_un_pedido_descuenta_el_stock_del_producto`, `test_se_cancela_un_pedido_si_esta_pendiente_de_envio`, `test_se_envia_un_pedido_si_esta_pendiente`.
- **Regla práctica:** cada comportamiento con al menos un test de "funciona" y uno por cada "no se puede".

### Cobertura indirecta
Un comportamiento está probado "de rebote" por un test que en realidad apunta a otra cosa.
- **Dónde:** antes de ORDERS-4, `ship()` (PENDING → SHIPPED) solo estaba cubierto por `test_no_se_puede_cancelar_un_pedido_que_ya_fue_enviado`: si `ship()` no cambiaba el estado, `cancel()` no lanzaba y ese test fallaba.
- **Problema:** cuando falla, el nombre y el error hablan de `cancel()`, y cuesta encontrar que la causa está en `ship()`. Por eso se sumó un test directo.

### Ver fallar un test
Un test que nunca viste en rojo puede estar pasando por casualidad. Si lo escribís sobre código que ya funciona (no es TDD puro), **rompé el código a propósito**, confirmá que se pone rojo y volvé a dejarlo como estaba.
- **Dónde:** `test_se_envia_un_pedido_si_esta_pendiente` (comentar `self.status = OrderStatus.SHIPPED` en `ship()`).

### Nombres de test que dicen la verdad
Cuando un test falla, lo primero que se lee es su nombre. Tiene que describir **lo que prueba**, incluido si es un "no se puede".
- **Dónde:** `test_se_envia_un_pedido_ya_enviado` → `test_no_se_reenvia_un_pedido_ya_enviado`; `test_crear_un_pedido_con_stock_insuficiente_del_producto` → `..._con_cantidad_invalida_...` (probaba `quantity=-1`, no falta de stock).

---

## Diseño y Python

### Arquitectura hexagonal (puertos y adaptadores)
El dominio (reglas de negocio) en el centro, sin saber nada de HTTP ni de bases de datos. Lo de afuera (API, DB) se conecta por adaptadores.
- **Dónde:** `src/domain/` (centro), `src/use_cases/` (orquestación), `src/adapters/` (FastAPI, repositorios). Ver `README.md`.
- **Señal de alarma:** tener que tocar `domain/` para que ande la API.

### `@dataclass`
Genera el `__init__` (y `__repr__`, `__eq__`) a partir de los atributos tipados. → decisión 2.
- **Dónde:** `Product` (`src/domain/product.py`), `Order` (`src/domain/order.py`).

### Factory method con `@classmethod`
Un método de **clase** (recibe `cls`, no `self`) que valida y después construye. → decisión 3.
- **Dónde:** `Order.create(product, quantity)`.

### Métodos de instancia
Reciben `self` y operan sobre **un** objeto ya creado, cambiando su estado.
- **Dónde:** `order.ship()`, `order.cancel()`.
- **Diferencia con `create`:** `Order.create(...)` se llama sobre la clase (todavía no hay pedido); `order.ship()` sobre un pedido concreto.

### Excepciones de dominio
Clases de excepción propias para cada regla de negocio violada, para que quien llama sepa **qué** salió mal. → decisión 4.
- **Dónde:** `src/domain/exceptions.py`.
- **Convención:** terminan en `Error` (PEP 8). → decisión 7.

### `Enum`
Conjunto cerrado de valores con nombre. Un typo (`OrderStatus.SHIPED`) explota al momento, cosa que con un string suelto (`"shiped"`) no pasa. → decisión 6.
- **Dónde:** `OrderStatus` en `src/domain/enum.py`.

### `from __future__ import annotations`
Permite que un método de `Order` declare `-> Order` sin comillas. → decisión 5.
- **Dónde:** primera línea de `src/domain/order.py`.

### Guard clause
Chequear primero los casos prohibidos y cortar con `raise` (o `return`); el caso normal queda al final, sin `if`. → decisión 8.
- **Dónde:** `Order.ship()`.
```python
if self.status == OrderStatus.CANCELLED:
    raise OrderCancelledCannotBeShippedError(...)
if self.status == OrderStatus.SHIPPED:
    raise OrderShippedCannotBeShippedAgainError(...)
self.status = OrderStatus.SHIPPED
```

### Fallo silencioso
Una operación que no hace lo pedido y **no avisa**; quien la llamó cree que funcionó.
- **Dónde:** `ship()` antes de ORDERS-4 (sobre un pedido cancelado no hacía nada) y antes de ORDERS-5 (sobre uno ya enviado, tampoco).

### Idempotencia
Una operación es idempotente si hacerla una o varias veces deja el mismo resultado, sin error. Clave cuando hay reintentos (se corta la red y el cliente reenvía). → decisión 9.
- **Dónde:** se consideró para `ship()` sobre un pedido `SHIPPED`; se eligió lanzar excepción. Vuelve en la API REST (`GET`/`PUT`/`DELETE` son idempotentes, `POST` no) y en la Fase 2 (*idempotency keys*).

---

## Herramientas

### `venv` e intérprete de VS Code
Cada proyecto tiene su propio entorno virtual con sus dependencias.
- **Dónde:** `fase1-orders-api/venv/`. Tests: `./venv/bin/pytest -q` (o `source venv/bin/activate` y `pytest`).
- Si el editor marca `import pytest` como faltante, no se tapa con `# pyright: ignore`: se elige el intérprete del venv con `Ctrl+Shift+P` → "Python: Select Interpreter". Se guarda **por workspace** (la carpeta abierta), no para todo el perfil. Para dejarlo fijo: `.vscode/settings.json` con `python.defaultInterpreterPath`.

### Autoimports del editor
Al escribir un nombre, el editor puede agregar un import que no pediste.
- **Dónde:** apareció `from itertools import product` en `test_order.py` al escribir la variable `product`.

### ruff
Linter de Python. Con la configuración actual **no** detecta espacios al final de línea (regla `W293`, no activa por defecto); sí marca orden de imports (`I001`). `ruff check .` para ver, `ruff check --fix .` para arreglar lo automático.

### `gh` (GitHub CLI) e issues
- `gh issue list --state all` — ver todos los tickets.
- `gh issue view N --json title,body --jq '.title, "", .body'` — leer uno. (`gh issue view N` a secas falla en este repo por un error de GitHub con Projects clásicos.)
- Un commit con `Closes #N` en el mensaje cierra el issue al pushearlo a `main`.
- Un commit por ticket: si en el medio aparece algo fuera de alcance, va en su propio ticket y commit (así nació ORDERS-5).
