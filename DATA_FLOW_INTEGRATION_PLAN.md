# Image Analyzer System: Data Flow Analysis & Integration Plan

## Executive Summary

This document analyzes the current data flow between modules in the Image Analyzer system and proposes a detailed development plan to connect isolated components into a fully integrated pipeline.

> [!IMPORTANT]
> **Current State**: All 4 modules operate in complete isolation. Integration infrastructure exists but is NOT wired up to any module backends. No data flows between systems despite the intended architecture.

---

## Current System Architecture

### Module Inventory

| Module | Backend | Database | Port | Status |
|--------|---------|----------|------|--------|
| **graphical-model** | FastAPI | PostgreSQL | 8000/8001 | ✅ Functional, isolated |
| **image-tagger** | FastAPI | PostgreSQL | 8080/8002 | ✅ Functional, isolated |
| **article-eater** | FastAPI | SQLite | 8000/8003 | ✅ Functional, isolated |
| **knowledge-graph-ui** | FastAPI | In-memory | 8000/8004 | ⚠️ Demo data only |

### Intended Data Flow (Not Implemented)

```mermaid
flowchart LR
 subgraph "Data Sources"
 AE[Article Eater<br/>Findings & Rules]
 IT[Image Tagger<br/>Tags & Attributes]
 end
 
 subgraph "Knowledge Layer"
 KG[Knowledge Graph UI<br/>Causal Edges + Evidence]
 end
 
 subgraph "Inference Engine"
 GM[Graphical Model<br/>Bayesian Predictions]
 end
 
 AE -->|"❌ NOT CONNECTED"| KG
 IT -->|"❌ NOT CONNECTED"| GM
 KG -->|"❌ NOT CONNECTED"| GM
 GM -->|"❌ NOT CONNECTED"| KG
```

---

## Detailed Module Analysis

### 1. Article Eater (`article-eater/`)

**Purpose**: Extract findings from academic papers, cluster into design rules, build knowledge networks.

**Data Produced**:
- Seven-panel structured findings (study metadata, methods, effect sizes, mechanisms)
- Aggregated design rules with confidence weights
- BN Export format ([BN_EXPORT_SCHEMA_v0_1.md](file:///Users/taggertsmith/Desktop/Image_Analyzer/article-eater/Article_Eater_v20_7_43_repo/docs/BN_EXPORT_SCHEMA_v0_1.md)) with nodes/edges/rules

**Current Database**: SQLite (`ae.db`)

**Key API Endpoint**: `POST /api/admin/rulegraph_v2/export_bn`

**Export Schema**:
```json
{
 "bn_version": "0.2",
 "nodes": [{"id": "trait:SPS", "type": "subject_trait", "label": "SPS"}],
 "edges": [{"from": "trait:SPS", "to": "rule:Ulrich_1984:R1", "type": "subject_scope"}],
 "rules": [{"rule_id": "R1", "paper_id": "Ulrich_1984", "rule_text": "...", "evidence": {...}}]
}
```

> [!WARNING]
> **Isolation Status**: No integration with knowledge-graph-ui. BN export exists but no consumer uses it. Findings stored in SQLite, not shared PostgreSQL.

---

### 2. Image Tagger (`image-tagger/`)

**Purpose**: Enterprise image tagging system for architectural research with VLM integration.

**Data Produced**:
- Image attributes (visual features via science pipeline)
- Human tags and annotations
- IRR (Inter-Rater Reliability) metrics
- Composite indices for BN modeling

**Current Database**: PostgreSQL (separate instance, not shared)

**Architecture**: 4 React micro-frontends (Workbench, Monitor, Admin, Explorer)

**Key Data Types**:
- Visual complexity scores (Canny edge detection)
- Semantic tags from VLM or human raters
- Binned attribute values (low/medium/high)

> [!WARNING]
> **Isolation Status**: No connection to graphical-model. Tagged attributes not exported for Bayesian inference training. Science pipeline outputs stay within image-tagger.

---

### 3. Knowledge Graph UI (`knowledge-graph-ui/`)

**Purpose**: Interactive visualization of causal relationships between attributes, mediators, and outcomes.

**Data Structure**:
- **Nodes**: Attributes (top), Mediators (middle), Outcomes (bottom)
- **Edges**: Causal relationships with effect sizes, CIs, and literature evidence
- **Evidence Items**: DOIs, study summaries, populations, designs

**Current Database**: **IN-MEMORY ONLY** (hardcoded demo data)

The backend has infrastructure for PostgreSQL loading but defaults to static demo data:

```python
# From main.py - demo edges defined in code
NODES: List[GraphNode] = [...] # Hardcoded
EDGES: Dict[str, EdgeDetail] = {} # Populated by register_edge calls

# Database loading exists but DATABASE_STATUS defaults to "unconfigured"
DATABASE_GRAPH: Optional[Tuple[...]] = None
```

**Prediction Endpoint** (`POST /predict`): Deterministic formulas, NOT Bayesian inference:
```python
perceived_warmth = 0.3 + 0.8 * w - 0.2 * glare # Simple linear, not model output
```

> [!CAUTION]
> **Critical Issue**: Knowledge-graph-ui uses demo data and deterministic predictions. Not connected to real literature evidence from article-eater or real Bayesian inference from graphical-model.

---

### 4. Graphical Model (`graphical-model/`)

**Purpose**: Bayesian causal modeling for predicting psychological outcomes from image attributes.

**Statistical Engine**:
- `model_a.py`: Attributes → Mediators (Goldilocks functions, PyMC)
- `model_b.py`: Mediators → Outcomes (Do-calculus, causal inference)
- `pipeline.py`: End-to-end prediction with uncertainty propagation

**Current Database**: PostgreSQL (`image_psychology`)

**Key API Endpoints**:
- `POST /api/v1/predict` - Run predictions from attributes
- `POST /api/v1/intervene` - What-if interventions
- `GET /api/v1/images` - Image management

**Training Status**: Uses synthetic data only. No real training data from image-tagger.

> [!WARNING]
> **Isolation Status**: Models exist but not trained on real data. No integration with image-tagger for training data or knowledge-graph for causal structure.

---

### 5. Integration Layer (`integration/`)

**Purpose**: Unified infrastructure for connecting all modules.

**What Exists (Built but Not Connected)**:

| Component | File/Directory | Status |
|-----------|----------------|--------|
| Docker Orchestration | [docker-compose.unified.yml](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/docker-compose.unified.yml) | ✅ Complete |
| Shared PostgreSQL Schemas | [db-init/](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/db-init) | ✅ Complete |
| Redis Event Publisher | [shared/events/publisher.py](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/shared/events/publisher.py) | ✅ Complete |
| Event Schemas | [shared/events/schemas.py](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/shared/events/schemas.py) | ✅ Complete |
| Auth Service | [shared/auth/](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/shared/auth) | ✅ Complete |
| API Client | [shared/api_client/](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/shared/api_client) | ✅ Complete |
| Frontend Shell | [frontend-shell/](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/frontend-shell) | ✅ Complete (React/Vite) |
| Nginx Gateway | [nginx/nginx.conf](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/nginx) | ✅ Complete |

**Database Schemas Created**:
- `core` - Shared users, images, literature_sources
- `tagger` - Image-tagger specific (raters, attributes, tags)
- `evidence` - Article-eater specific (articles, findings, rules)
- `graphical` - Graphical-model specific (model_runs, predictions)
- `graph` - Knowledge-graph specific (nodes, edges, edge_evidence)

> [!NOTE]
> **Critical Gap**: Integration infrastructure is 100% built but 0% used. No module imports `integration.shared`. Each module uses its own isolated database and has no event publishing.

---

## What's Broken vs What's Missing

### Broken (Infrastructure exists, not wired)

| Issue | Impact | Files Involved |
|-------|--------|----------------|
| Modules don't use shared PostgreSQL | Data silos, no cross-referencing | Each module has own DB config |
| Event bus not imported by any module | No real-time updates between modules | `integration/shared/events/*` unused |
| Frontend shell uses iframes, no data sharing | UI navigation works, data doesn't flow | `frontend-shell/src/modules/*.jsx` |
| Knowledge-graph uses in-memory data | Cannot display real evidence from article-eater | `knowledge-graph-ui/.../main.py` |

### Missing (Not implemented at all)

| Feature | Required For | Complexity |
|---------|--------------|------------|
| Article-eater → Knowledge-graph sync | Update causal edges with new findings | Medium |
| Image-tagger → Graphical-model export | Train Bayesian models on real tags | Medium |
| Graphical-model → Knowledge-graph feedback | Update posterior edge effects | Low |
| Knowledge-graph → Graphical-model structure | Share causal DAG for inference | Low |
| Cross-module authentication | Single sign-on | Low (auth service exists) |

---

## Proposed Implementation Plan

### Phase 1: Database Migrations & Backend Alignment (3-4 days)

> [!IMPORTANT]
> All modules must migrate to the shared PostgreSQL database with proper schema prefixes.

#### 1.1 Migrate Article-Eater from SQLite to PostgreSQL

**Files to Modify**:
- [app/db.py](file:///Users/taggertsmith/Desktop/Image_Analyzer/article-eater/Article_Eater_v20_7_43_repo/app/db.py) - Database connection
- [init_database.py](file:///Users/taggertsmith/Desktop/Image_Analyzer/article-eater/Article_Eater_v20_7_43_repo/init_database.py) - Schema initialization

**Changes**:
```diff
- DB_URL = os.getenv("DB_URL", "sqlite:///./ae.db")
+ DB_URL = os.getenv("DB_URL", "postgresql://postgres:devpassword@localhost:5432/image_analyzer")
+ SCHEMA_NAME = os.getenv("SCHEMA_NAME", "evidence")
```

---

#### 1.2 Configure Knowledge-Graph for Database Backend

**Files to Modify**:
- [backend/app/main.py](file:///Users/taggertsmith/Desktop/Image_Analyzer/knowledge-graph-ui/GraphExplorer_Static_v3/backend/app/main.py)

**Changes**:
- Set `DATABASE_URL` environment variable in docker-compose
- Ensure `SCHEMA_NAME=graph` for proper schema
- Seed `graph.nodes` and `graph.edges` tables with initial demo data

---

#### 1.3 Align Image-Tagger with Shared Schema

**Files to Modify**:
- Backend database configuration
- Add foreign keys to `core.images` and `core.users`

---

### Phase 2: Article-Eater → Knowledge-Graph Pipeline (4-5 days)

#### 2.1 Create Evidence Export API in Article-Eater

**[NEW] File**: `article-eater/.../routes/integration.py`

```python
@router.post("/integration/export-to-graph")
async def export_findings_to_graph:
 """Export extracted findings in format for knowledge-graph edges."""
 findings = db.get_recent_findings
 return [
 {
 "edge_id": f"{f.cause_node}->{f.effect_node}",
 "from_node": f.cause_node,
 "to_node": f.effect_node,
 "effect_size": f.effect_size,
 "effect_direction": f.direction,
 "evidence": {
 "doi": f.paper_doi,
 "title": f.paper_title,
 "population": f.population,
 "quality": f.quality_score
 }
 }
 for f in findings
 ]
```

---

#### 2.2 Create Evidence Import API in Knowledge-Graph

**[MODIFY]** [backend/app/main.py](file:///Users/taggertsmith/Desktop/Image_Analyzer/knowledge-graph-ui/GraphExplorer_Static_v3/backend/app/main.py)

```python
@app.post("/api/v1/edges/update-from-findings")
def update_edges_from_findings(findings: List[FindingInput]):
 """Receive new evidence from article-eater and update edge posteriors."""
 for finding in findings:
 edge = EDGES.get(finding.edge_id) or create_new_edge(finding)
 edge.evidence.append(finding.to_evidence_item)
 # Update effect size posterior with new evidence
 edge.param = update_posterior(edge.param, finding.effect_size, finding.weight)
 
 # Publish event for other modules
 event_bus.publish("graph:edges_updated", {"edge_ids": [f.edge_id for f in findings]})
 return {"updated": len(findings)}
```

---

#### 2.3 Wire Redis Event Bus

**[MODIFY]** Both article-eater and knowledge-graph backends:

```python
from integration.shared.events import RedisEventPublisher, EventMessage

publisher = RedisEventPublisher

# In article-eater after finding extraction:
publisher.publish("evidence:finding_extracted", EventMessage.create(event_type="finding_extracted",
 source_module="article-eater",
 payload={"finding_id": finding.id, "edge_candidates": [...]}))

# In knowledge-graph as subscriber:
subscriber.subscribe("evidence:finding_extracted", handle_new_evidence)
```

---

### Phase 3: Image-Tagger → Graphical-Model Pipeline (4-5 days)

#### 3.1 Create BN Training Data Export in Image-Tagger

**[NEW] File**: `image-tagger/.../routers/integration.py`

```python
@router.get("/v1/export/bn-training-data")
async def export_bn_training_data(format: str = "json"):
 """Export tagged image attributes for Bayesian network training."""
 images = await db.get_images_with_complete_tags
 return {
 "version": "1.0",
 "images": [
 {
 "image_id": img.id,
 "attributes": {
 "wood_coverage": img.attrs.wood_coverage,
 "plant_density": img.attrs.plant_density,
 "spatial_clutter": img.attrs.spatial_clutter,
 #... all visual attributes
 },
 "mediator_ratings": img.aggregate_ratings,
 "outcome_ratings": img.aggregate_outcomes
 }
 for img in images
 ]
 }
```

---

#### 3.2 Create Training Data Import in Graphical-Model

**[MODIFY]** [api/routes/admin.py](file:///Users/taggertsmith/Desktop/Image_Analyzer/graphical-model/api/routes/admin.py)

```python
@router.post("/integration/import-training-data")
async def import_training_data(data: TrainingDataImport):
 """Import tagged images from image-tagger for model training."""
 # Save to database
 for image in data.images:
 await db.upsert_training_sample(image)
 
 # Optionally trigger retraining
 if data.trigger_retrain:
 background_tasks.add_task(retrain_models)
 
 return {"imported": len(data.images), "status": "queued"}
```

---

### Phase 4: Knowledge-Graph ↔ Graphical-Model Bidirectional Flow (3-4 days)

#### 4.1 Export Causal Structure from Knowledge-Graph

```python
@app.get("/api/v1/graph/export-for-bayesian")
def export_for_bayesian:
 """Export graph structure for graphical-model DAG specification."""
 return {
 "nodes": [n.dict for n in NODES],
 "edges": [
 {
 "from": e.from_node,
 "to": e.to_node,
 "prior_mean": e.param.mean,
 "prior_sd": e.param.sd,
 "status": e.status
 }
 for e in EDGES.values
 ]
 }
```

---

#### 4.2 Import Updated Posteriors from Graphical-Model

```python
# In graphical-model after model fitting:
@router.post("/integration/publish-posteriors")
async def publish_posteriors(model_version: str):
 """Publish updated effect sizes back to knowledge-graph."""
 posteriors = await get_model_posteriors(model_version)
 
 # Call knowledge-graph API
 async with httpx.AsyncClient as client:
 await client.post(f"{KNOWLEDGE_GRAPH_URL}/api/v1/edges/update-from-posteriors",
 json=posteriors)
 return {"published": len(posteriors)}
```

---

### Phase 5: Frontend Integration & Testing (3-4 days)

#### 5.1 Update Frontend Shell Module Components

Replace iframe-based isolation with data-aware components:

**[MODIFY]** [frontend-shell/src/modules/KnowledgeGraph.jsx](file:///Users/taggertsmith/Desktop/Image_Analyzer/integration/frontend-shell/src/modules/KnowledgeGraph.jsx)

```jsx
// Instead of iframe, use API calls to fetch real data
export default function KnowledgeGraph({ gateway }) {
 const [graph, setGraph] = useState(null);
 
 useEffect(=> {
 fetch(`${gateway}/api/graph/v1_demo`).then(res => res.json).then(setGraph);
 }, [gateway]);
 
 // Render with real data, not iframe
 return <CytoscapeGraph data={graph} />;
}
```

---

## Verification Plan

### Automated Tests

| Test | Command | Purpose |
|------|---------|---------|
| Integration events | `pytest integration/tests/test_events.py -v` | Verify Redis pub/sub |
| API client | `pytest integration/tests/test_api_client.py -v` | Verify unified client |
| Auth service | `pytest integration/tests/test_auth.py -v` | Verify shared auth |
| End-to-end | `pytest integration/tests/test_integration.py -v` | Full pipeline test |

### Manual Verification Workflow

1. **Start unified infrastructure**:
 ```bash
 cd integration
 docker compose -f docker-compose.unified.yml up -d
 ```

2. **Submit a paper in Article-Eater** (http://localhost:8003):
 - Process paper through L2 extraction
 - Verify findings appear in database

3. **Check Knowledge-Graph updates** (http://localhost:8004):
 - Navigate to Causal Graph
 - Verify new evidence appears on edges
 - Check DOIs are clickable

4. **Tag an image in Image-Tagger** (http://localhost:8002):
 - Upload and tag image with attributes
 - Verify tags export to training data

5. **Run prediction in Graphical-Model** (http://localhost:8001):
 - Submit attributes from tagged image
 - Verify prediction uses trained model
 - Check uncertainty intervals

6. **Observe event flow in logs**:
 ```bash
 docker compose logs -f | grep -E "(evidence:|graph:|image:)"
 ```

---

## Estimated Effort

| Phase | Days | Dependencies |
|-------|------|--------------|
| Phase 1: Database Migrations | 3-4 | None |
| Phase 2: Article-Eater → Knowledge-Graph | 4-5 | Phase 1 |
| Phase 3: Image-Tagger → Graphical-Model | 4-5 | Phase 1 |
| Phase 4: Bidirectional Flow | 3-4 | Phase 2, 3 |
| Phase 5: Frontend & Testing | 3-4 | Phase 4 |

**Total: 17-22 days**

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Database migration data loss | Full backup before migration, test on staging first |
| Breaking existing module APIs | Version APIs, maintain backwards compatibility |
| Event bus reliability | Implement retry logic, dead-letter queue |
| Frontend integration complexity | Start with iframe + postMessage, migrate incrementally |

---

## Summary of Key Integration Points

```mermaid
flowchart TB
 subgraph "Phase 2"
 AE_API[Article Eater<br/>POST /integration/export-to-graph]
 KG_IMPORT[Knowledge Graph<br/>POST /edges/update-from-findings]
 AE_API -->|HTTP| KG_IMPORT
 end
 
 subgraph "Phase 3"
 IT_API[Image Tagger<br/>GET /export/bn-training-data]
 GM_IMPORT[Graphical Model<br/>POST /integration/import-training-data]
 IT_API -->|HTTP| GM_IMPORT
 end
 
 subgraph "Phase 4"
 KG_EXPORT[Knowledge Graph<br/>GET /graph/export-for-bayesian]
 GM_STRUCT[Graphical Model<br/>Use for DAG structure]
 GM_POST[Graphical Model<br/>POST /integration/publish-posteriors]
 KG_UPDATE[Knowledge Graph<br/>POST /edges/update-from-posteriors]
 
 KG_EXPORT --> GM_STRUCT
 GM_POST --> KG_UPDATE
 end
 
 subgraph "Event Bus (All Phases)"
 REDIS[(Redis)]
 REDIS -.->|evidence:finding_extracted| KG_IMPORT
 REDIS -.->|graph:edges_updated| GM_STRUCT
 REDIS -.->|image:tagged| GM_IMPORT
 end
```
