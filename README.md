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
 /api/graphical -> graphical-model:8001
 /api/tagger -> image-tagger:8002
 /api/article -> article-eater:8003
 /api/graph -> knowledge-graph:8004
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

- **Causal reasoning, not just correlations**: the graphical-model is built around Bayesian causal inference and interventional queries (Pearl,).
- **Evidence-grounded design rules**: article-eater structures findings into auditable rules with provenance and quality metadata (Guyatt et al.,).
- **Human + machine tagging loop**: the tagger’s deterministic science pipeline supports repeatable feature extraction for controlled studies.
- **Graph exploration with evidence**: the knowledge graph UI connects edges to effect sizes and underlying sources, enabling evidence inspection.
- **Cross-module integration**: a unified system lets teams move from papers to predictions without context-switching tools.

## Scientific Foundations (Demo Summary)

This demo follows an academic architecture developed for evidence-based design, emphasizing interpretability, causal identification, and uncertainty transparency.

- **Three-layer model**: attributes (image-derived) -> mediators (perceived states) -> outcomes (psychological measures), supporting mechanistic interpretation.
- **Goldilocks effects**: key environmental attributes are modeled with inverted-U responses, preventing linear overgeneralization in design recommendations.
- **Bayesian evidence synthesis**: priors are informed by literature and updated with new data, yielding credible intervals rather than point claims.
- **Uncertainty classes**: structural, causal identification, heterogeneity, parametric, and model specification uncertainties are tracked separately.
- **Triangulation**: multiple study designs are combined to strengthen causal confidence when biases differ across methods (Munafò & Davey Smith,).

## Citations (Selected)

- Boubekri, M., Cheung, I. N., Reid, K. J., Wang, C. H., & Zee, P. C.. Impact of windows and daylight exposure on overall health and sleep quality of office workers. Journal of Clinical Sleep Medicine, 10(6), 603–611. https://doi.org/10.5664/jcsm.3780
- Gignac, G. E., & Szodorai, E. T.. Effect size guidelines for individual differences researchers. Personality and Individual Differences, 102, 74–78. https://doi.org/10.1016/j.paid..06.069
- Guyatt, G. H., et al.. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ, 336(7650), 924–926. https://doi.org/10.1136/bmj.39489.470347.AD
- Lewin, S., et al.. Applying GRADE-CERQual to qualitative evidence synthesis findings. Implementation Science, 13(S1), 2. https://doi.org/10.1186/s13012-017-0688-3
- Lohr, V. I., Pearson-Mims, C. H., & Goodwin, G. K.. Interior plants may improve worker productivity and reduce stress. Journal of Environmental Horticulture, 14(2), 97–100. https://doi.org/10.24266/0738-2898-14.2.97
- Munafò, M. R., & Davey Smith, G.. Robust research needs many lines of evidence. Nature, 553(7689), 399–401. https://doi.org/10.1038/d41586-018-01023-3
- Pearl, J.. Causality: Models, reasoning, and inference (2nd ed.). Cambridge University Press.
- Ulrich, R. S.. View through a window may influence recovery from surgery. Science, 224(4647), 420–421. https://doi.org/10.1126/science.6143402

## Important Notes

- The graphical model uses synthetic or mock data unless you supply real datasets.
- Many modules support mock or classroom-friendly modes by default.
- This is a research demo; guardrails for full deployment are out of scope.

## Repo Layout (Top Level)

```
integration/ # Unified demo orchestration and shared assets
graphical-model/ # Bayesian causal modeling system
image-tagger/ # Image tagging suite (micro-frontends + API)
article-eater/ # Literature evidence extraction
knowledge-graph-ui/ # Causal graph visualization
```
