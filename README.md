# Image Analyzer (Unified Demo)

Unified demo environment that stitches four research modules into a single system for evidence-driven architectural analysis.

This demo is built for scientists and architects who want a shared surface where:
- findings from the literature become structured evidence,
- evidence becomes causal graphs,
- tagged images become model inputs, and
- the causal model produces interpretable predictions.

It is an integration demo, not a production deployment.

## System Goals

1. Provide a single URL that exposes the four module UIs.
2. Standardize API routing through a gateway.
3. Share a single PostgreSQL database with schema isolation.
4. Demonstrate cross-module data flow (evidence -> graph -> model, tags -> model).
5. Keep the UI consistent with the article-eater and image-tagger styling.

## Architecture Overview

```
Unified Frontend Shell (Nginx + static assets)
           |
           v
API Gateway (Nginx reverse proxy, http://localhost:8080)
  /api/graphical  -> graphical-model:8001
  /api/tagger     -> image-tagger:8002
  /api/article    -> article-eater:8003
  /api/graph      -> knowledge-graph:8004
           |
           v
Shared PostgreSQL + Redis
  schemas: core, tagger, evidence, graphical, graph
```

## Included Modules

- **graphical-model**: Bayesian causal model with do-calculus and uncertainty.
- **image-tagger**: micro-frontend tagging suite and deterministic science pipeline.
- **article-eater**: evidence extraction with seven-panel schema and BN export.
- **knowledge-graph-ui**: causal graph visualization and evidence inspection.

## Demo Quickstart

```bash
# From repo root
docker compose -f integration/docker-compose.unified.yml up -d
```

Open the unified shell:
- http://localhost:8080

Module surfaces (via the shell):
- Tagger workbench: `http://localhost:8080/workbench/`
- Article eater UI: `http://localhost:8080/article/`
- Knowledge graph: `http://localhost:8080/graph/`
- Graphical model UI: `http://localhost:8080/graphical/`

Health checks:
- `http://localhost:8080/api/graphical/health`
- `http://localhost:8080/api/tagger/health`
- `http://localhost:8080/api/article/health`
- `http://localhost:8080/api/graph/health`

## What Makes This Useful for Scientists and Architects

- **Causal reasoning, not just correlations**: the graphical-model uses Bayesian causal inference with explicit mediation layers.
- **Evidence-grounded design rules**: article-eater structures findings into rules with provenance and quality metadata.
- **Human + machine tagging loop**: tagger provides a repeatable tagging workflow with deterministic science methods.
- **Graph exploration with evidence**: the knowledge graph UI connects edges to literature and effect sizes.
- **Cross-module integration**: a unified system lets a research team move from papers to predictions without context-switching tools.

## Important Notes

- The graphical model uses synthetic or mock data unless you supply real datasets.
- Many modules support mock or classroom-friendly modes by default.
- This is a research demo; guardrails for full deployment are out of scope.

## Repo Layout (Top Level)

```
integration/           # Unified demo orchestration and shared assets
graphical-model/       # Bayesian causal modeling system
image-tagger/          # Image tagging suite (micro-frontends + API)
article-eater/         # Literature evidence extraction
knowledge-graph-ui/    # Causal graph visualization
```
