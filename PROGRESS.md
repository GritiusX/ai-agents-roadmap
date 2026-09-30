# Progreso — Bitácora AI Agents

Registro de avance real, fase por fase. Espejo del roadmap interactivo (bitácora en Claude), pero acá queda commiteado junto con el código.

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
- [ ] **ORDERS-4**: no se puede enviar un pedido cancelado — en curso
- [ ] Exponer todo vía API REST con FastAPI + OpenAPI
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
