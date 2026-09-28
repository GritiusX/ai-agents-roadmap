# Orders API — Fase 1

API de gestión de pedidos con control de stock. Proyecto de práctica para aplicar arquitectura limpia, SOLID y TDD (Fase 1 de la bitácora AI Agents).

## Estructura

```
src/
  domain/        → entidades y reglas de negocio puras (Product, Order, excepciones). Sin imports de FastAPI ni de DB.
  use_cases/      → orquestan el dominio (todavía sin uso, llega con el primer endpoint)
  adapters/
    api/          → rutas de FastAPI (todavía sin uso)
tests/
  domain/         → tests de las reglas de negocio
```

## Cómo correr los tests

```bash
source venv/bin/activate
pytest
```

## Decisiones técnicas

Ver [`docs/decisions.md`](./docs/decisions.md) para el detalle de por qué se tomó cada decisión (patrón factory con `@classmethod`, dataclasses, excepciones de dominio propias, etc.).

## Estado

Ver [`../PROGRESS.md`](../PROGRESS.md) para el checklist de qué está hecho y qué falta.
