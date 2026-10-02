# Progreso — Bitácora AI Agents

Registro de avance real, fase por fase. Espejo del roadmap interactivo (bitácora en Claude), pero acá queda commiteado junto con el código.

**Estado (2026-10-02):** bitácora en pausa, prioridad conseguir trabajo.

Conceptos aprendidos en el camino (con dónde aparecen en el código): [`GLOSARIO.md`](./GLOSARIO.md)

## Fase 0 — Diagnóstico y setup
- [x] Mapear el aviso de MELI contra la experiencia actual
- [x] Python 3.12 instalado (ya venía en el sistema)
- [x] ruff y mypy instalados (vía pipx, para uso global del editor)
- [x] Repo "ai-agents-roadmap" creado y pusheado a GitHub
- [ ] Sumarse a 2-3 comunidades (Discord de Anthropic/LangChain, foros de tech Argentina)

## Fase 1 — Backend con criterio
Proyecto: [`fase1-orders-api/`](./fase1-orders-api) — API de gestión de pedidos con control de stock.

- [x] Proyecto creado con `venv` + FastAPI + uvicorn + pytest
- [x] Estructura de arquitectura hexagonal (`domain/`, `use_cases/`, `adapters/`)
- [x] **ORDERS-1**: no se puede crear un pedido sin stock suficiente (TDD, rojo→verde)
- [x] **ORDERS-2**: rechazar pedidos con cantidad inválida (0 o negativa)
- [x] **ORDERS-3**: no se puede cancelar un pedido ya enviado (estado con `Enum`, métodos de instancia)
- [x] **ORDERS-4**: no se puede enviar un pedido cancelado (+ test del camino feliz de `ship()`)
- [x] **ORDERS-5**: no se puede reenviar un pedido ya enviado (excepción en vez de idempotencia)
- [ ] Exponer todo vía API REST con FastAPI + OpenAPI
  - [ ] **ORDERS-6**: repositorio en memoria + caso de uso para crear pedidos — en pausa (3 de 6 pasos: repos de pedidos y productos + `CreateOrder`; sigue: excepción si el `product_id` no existe)
  - [ ] **ORDERS-7**: `POST /orders` y `GET /orders/{id}`
  - [ ] **ORDERS-8**: excepciones de dominio → códigos HTTP
  - [ ] **ORDERS-9**: endpoints para enviar y cancelar pedidos
- [ ] Migraciones con Alembic + Postgres

Detalle de decisiones técnicas de este proyecto: [`fase1-orders-api/docs/decisions.md`](./fase1-orders-api/docs/decisions.md)

## Fase 2 — Sistemas distribuidos
No arrancada.

## Fase 3 — LLMs, agentes y evaluación
No arrancada.

## Fase 4 — Proyecto insignia
No arrancada.

## Fase 5 — Preparación de entrevistas
No arrancada.

## Fase 6 (Google) — Cloud AI Engineer
No arrancada — horizonte siguiente, no en paralelo.
