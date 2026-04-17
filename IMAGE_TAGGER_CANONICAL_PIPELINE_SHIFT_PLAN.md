# Image Tagger Canonical Pipeline Shift Plan

## Purpose

This document defines a concrete implementation plan for shifting the `image-tagger` architecture from its current split model:

- persisted scalar science attributes in `Validation`
- runtime-only affordance cache in `Image.meta_data`
- runtime-only debug overlays and VLM visualizations
- mixed-source tags assembled ad hoc in the Explorer detail API

to a more coherent model in which:

- canonical, pipeline-derived tags and attributes are generated in the background
- previously processed images reuse stored outputs
- the Explorer detail UI shows a truthful, unified view of canonical science outputs
- only parameterized teaching/debug modes remain live/on-demand

This plan is intentionally detailed and assumes implementation in:

- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/`


## Executive Summary

The desired end state is:

1. When the Explorer app starts, it triggers backend orchestration that schedules science processing for images that do not yet have canonical outputs for the current science version.
2. The canonical science pipeline runs in the background and persists:
   - scalar science attributes
   - canonical pipeline-derived tags
   - canonical affordance outputs
   - canonical room-type outputs
   - canonical segmentation/object outputs
   - one canonical saved segmentation artifact
3. The Explorer detail view reads those persisted outputs first and presents them consistently:
   - `Tags` shows canonical imported and pipeline tags
   - `Science Attributes` shows the underlying scored attributes for those tags and models
   - debug-only views remain on-demand for non-canonical parameterizations
4. Debug endpoints remain available for:
   - edges
   - complexity
   - depth
   - segmentation at non-default thresholds / variants
   - other teaching views where parameter sensitivity matters

The central design rule is:

> Canonical science outputs must be generated once, versioned, persisted, and reused.
> Interactive debug outputs may still be computed on demand when they are inherently parameterized or pedagogical.


## Current State

### What exists now

- The science pipeline persists `frame.attributes` into `Validation` rows with `source="science_pipeline_v3.4"`.
  - File: `backend/science/pipeline.py`
- Explorer detail loads science attributes only from persisted `Validation` rows whose source starts with `science_pipeline`.
  - File: `backend/api/v1_discovery.py`
- Affordances are handled separately via a cached payload stored in `Image.meta_data["affordance_runtime_v1"]`.
  - File: `backend/api/v1_discovery.py`
- Debug overlays are served by `v1_debug` endpoints that compute artifacts directly from image pixels and return PNGs.
  - File: `backend/api/v1_debug.py`
- Explorer tags are currently assembled from:
  - imported metadata tags in `Image.meta_data.tags`
  - a subset of science attributes promoted into display tags at read time
  - File: `backend/api/v1_discovery.py`

### Resulting problems

1. The UI is conceptually inconsistent.
   - The `Science Attributes` section can be empty while tags, affordances, room views, materials, or overlays exist.

2. Canonical vs runtime outputs are mixed together without a clear contract.
   - Some outputs are persisted.
   - Some are cached in image metadata.
   - Some are recomputed every request.

3. There is no first-class persisted representation for canonical non-scalar outputs.
   - Segmentation/object results are not stored as canonical per-image science outputs.
   - Room-type outputs are not persisted as canonical attributes/tags.
   - Affordance values are not normalized into the same canonical science output model.

4. The detail endpoint synthesizes tags instead of reading a canonical tag store.

5. There is no clean notion of pipeline completeness per image for the current science version.


## Target Architecture

### Guiding principles

1. Persist canonical outputs; compute debug variants on demand.
2. Version all canonical outputs by science pipeline version and config fingerprint.
3. Treat Explorer startup as an orchestration trigger, not as the place where inference itself runs.
4. Keep the current `Validation` table for scalar auditability and downstream BN compatibility.
5. Add a first-class persisted store for richer pipeline outputs that do not fit naturally into `Validation`.
6. Avoid storing unnecessary binary artifacts; save only the canonical segmentation artifact initially.

### Canonical outputs to support in Phase 1

These must become canonical pipeline outputs:

- scalar science attributes already produced by the pipeline
- affordance scores
- room-type classification
- segmentation/object detection summary
- pipeline-derived tags for:
  - affordances
  - segmented objects
  - room type
  - existing semantic/cognitive tags where enabled
- one canonical saved segmentation artifact

### Debug-only outputs to keep live

These remain on-demand:

- edges
- complexity heatmap
- depth visualization
- segmentation overlays at non-default thresholds or alternate render modes
- any UI control whose value changes the output continuously or semi-continuously


## Canonical Data Model

The current data model is not sufficient by itself because `Validation` is excellent for scalar values but poor for richer per-image science outputs and artifact metadata.

### Keep

- `images`
- `validations`
- `upload_jobs`
- `upload_job_items`

### Add

#### 1. `science_runs`

Purpose:

- one row per image per canonical science version/config execution
- authoritative lifecycle state for pipeline completeness

Suggested columns:

- `id`
- `image_id`
- `science_version`
- `config_fingerprint`
- `status` (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `STALE`)
- `queued_at`
- `started_at`
- `completed_at`
- `error_message`
- `trigger_source` (`explorer_bootstrap`, `upload_job`, `manual_admin`, `backfill`)
- `is_current`

Recommended unique constraint:

- `(image_id, science_version, config_fingerprint)`

Why:

- removes ambiguity around whether an image has canonical outputs for the active pipeline
- prevents re-running identical work unnecessarily

#### 2. `science_artifacts`

Purpose:

- store metadata about saved canonical artifacts without storing binaries in the DB

Suggested columns:

- `id`
- `science_run_id`
- `image_id`
- `artifact_type` (`segmentation_mask_png`, `segmentation_json`, `room_json`, `affordance_json`)
- `storage_path`
- `content_type`
- `artifact_version`
- `meta_json`

Phase 1 requirement:

- only `segmentation_mask_png` must be stored as a binary artifact path
- JSON summaries may optionally be stored in files or in `meta_json`

#### 3. `science_tags`

Purpose:

- canonical pipeline tag table rather than synthesizing tags ad hoc at read time

Suggested columns:

- `id`
- `science_run_id`
- `image_id`
- `tag_key`
- `label`
- `namespace`
- `confidence`
- `source_analyzer`
- `attribute_key` nullable
- `is_canonical`

Recommended unique constraint:

- `(science_run_id, image_id, tag_key)`

Why:

- gives Explorer a stable tag source
- removes current read-time promotion logic as the primary mechanism
- supports provenance and filtering cleanly

#### 4. Optional: `science_output_cache` table

This is optional if artifact metadata and tags are sufficient.

Purpose:

- normalized storage for structured per-image output payloads that are not best represented as individual rows

Suggested uses:

- raw affordance score payload
- room top-k results
- object counts/coverage summary

If the team wants to minimize schema expansion, these can instead live in:

- `science_artifacts.meta_json`
- or `Image.meta_data["science_outputs_vX"]`

Recommendation:

- prefer explicit tables over stuffing new canonical state into `Image.meta_data`
- keep `Image.meta_data` for import/search metadata and transitional caches only


## Canonical Output Contract

### Scalar attributes

Persist as `Validation` rows, as today, but expand the pipeline so it writes canonical scalar outputs for:

- affordance scores as numeric values
  - e.g. `affordance.L059.sleep`
  - or `affordance.sleep`
- room type confidence values
  - e.g. `spatial.room_type.kitchen`
  - `spatial.room_type.living_room`
- segmentation/object scalar summaries
  - e.g. `segmentation.object.chair.count`
  - `segmentation.object.chair.coverage_ratio`
  - `segmentation.object.table.present`
- canonical semantic tags already expressed numerically
  - e.g. `style.minimalist`
  - `cognitive.restorative`

Rules:

- every canonical display tag should have an underlying numeric attribute or summary field
- `Science Attributes` should be able to explain every pipeline-derived tag shown in the UI

### Canonical tags

Canonical tags should be generated by the pipeline and persisted into `science_tags`.

Examples:

- `room_type.kitchen`
- `object.chair`
- `object.window`
- `affordance.sleep.high`
- `affordance.work.strong`
- `style.minimalist`

Important distinction:

- display tags should be derived once during the science run
- the read API should not invent new canonical tags from scratch

### Canonical segmentation artifact

Persist one canonical segmentation artifact per current science run:

- default threshold only
- default semantic/panoptic merge settings only
- path on disk/object storage
- associated artifact metadata

Recommended artifact bundle in Phase 1:

- PNG semantic mask or merged segmentation visualization
- JSON summary containing:
  - class labels
  - counts
  - confidence values
  - coverage ratios
  - bounding boxes if available

The JSON is strongly recommended because it is the real reusable source of truth for UI and downstream logic.


## Required Product Behavior

### Explorer startup

On Explorer app startup:

1. frontend calls a bootstrap endpoint once per session
2. backend checks whether there are images missing canonical outputs for the active science version/config
3. backend queues missing images for background processing
4. frontend continues loading immediately; it does not wait for the backlog to finish
5. detail/search endpoints return whatever canonical outputs already exist
6. optionally expose progress so the UI can say:
   - `Science backlog: 312 images pending`

Important:

- do not run the whole pipeline synchronously in the Explorer browser session
- the frontend should trigger orchestration, not inference

### Search/grid behavior

The Explorer search/grid should:

- use canonical tags when available
- continue showing imported metadata tags if present
- never require on-demand model execution just to render basic search results

### Detail modal behavior

For a processed image:

- `Tags` shows:
  - imported tags
  - canonical pipeline tags
- `Science Attributes` shows:
  - underlying numeric science attributes
  - affordance scores
  - room-type confidences
  - segmentation/object counts/coverage/confidence summaries

For an unprocessed image:

- the empty state must be accurate:
  - `Canonical science outputs have not been generated for this image yet.`

For a partially processed or failed image:

- show a precise state:
  - `Science run in progress`
  - `Science run failed`
  - `Canonical segmentation available; affordance pending`


## Backend Implementation Plan

## Phase 0: Define the canonical contract before writing code

### Deliverables

- finalize canonical attribute key naming
- finalize canonical tag namespaces
- finalize what qualifies as a canonical tag vs debug-only observation
- finalize artifact naming/versioning

### Decisions required

#### Affordances

Recommended:

- persist raw 1-7 scores as canonical attributes
  - `affordance.L059`
  - `affordance.L079`
  - `affordance.L091`
  - `affordance.L130`
  - `affordance.L141`
- optionally persist normalized 0-1 scores too if needed for UI consistency
- derive tags from thresholded bins
  - e.g. `affordance.sleep.high`

#### Room type

Recommended:

- persist top-k class confidences as canonical attributes
  - `spatial.room_type.kitchen`
  - `spatial.room_type.bedroom`
- emit one primary canonical tag
  - `room_type.kitchen`

#### Segmentation/objects

Recommended:

- persist scalar object summaries:
  - count
  - total mask coverage ratio
  - presence indicator
- emit tags for objects that pass canonical thresholds
  - `object.chair`
  - `object.window`

### File areas to touch

- `backend/science/features_registry.py`
- `backend/science/features_canonical.jsonl`
- `contracts/attributes.yml`
- `backend/data/goldilocks_attributes.csv`
- `docs/SCIENCE_TAG_MAP.md`

### Exit criteria

- every canonical tag has a corresponding canonical source of truth
- every persisted scalar key is present in the registry


## Phase 1: Add science-run orchestration and persistence primitives

### Goals

- establish authoritative state tracking
- eliminate ambiguity around whether an image has been processed

### Work items

1. Add models and migrations for:
   - `science_runs`
   - `science_artifacts`
   - `science_tags`

2. Add SQLAlchemy models under:
   - `backend/models/science_runs.py`
   - or equivalent naming

3. Add database migration script(s).
   - follow existing migration style in `backend/scripts/`

4. Add a service layer:
   - `backend/services/science_runs.py`

Core functions:

- `get_active_science_version()`
- `get_config_fingerprint()`
- `ensure_science_run(image_id, trigger_source)`
- `queue_missing_science_runs(image_ids | all_images)`
- `mark_run_started(run_id)`
- `mark_run_completed(run_id)`
- `mark_run_failed(run_id, error)`
- `get_current_run_for_image(image_id)`

### Design rules

- a completed run must be immutable for that version/config
- a new version/config creates a new run, not mutation of the old one
- `is_current` should identify the run the APIs should read by default

### Recommended storage strategy

- use filesystem/object storage for artifacts
- store paths and metadata in `science_artifacts`
- keep binaries out of PostgreSQL

### Exit criteria

- backend can answer: `does image X have current canonical science outputs?`
- backend can queue work without duplicating runs


## Phase 2: Refactor the science pipeline into canonical output producers

### Goals

- promote affordance, room type, and segmentation/object summaries into the canonical science pipeline
- preserve current scalar validation behavior for BN and audit workflows

### Work items

#### 2.1 Introduce a `ScienceRunContext`

Create a context object passed through the pipeline that collects:

- scalar attributes
- canonical tags
- artifacts to persist
- structured summaries

Suggested file:

- `backend/science/run_context.py`

Suggested shape:

```python
class ScienceRunContext:
    image_id: int
    science_version: str
    config_fingerprint: str
    attributes: dict[str, float]
    tags: list[ScienceTagRecord]
    artifacts: list[ScienceArtifactRecord]
    summaries: dict[str, Any]
```

This avoids overloading `AnalysisFrame.metadata` with canonical persistence semantics.

#### 2.2 Keep `AnalysisFrame`, but make pipeline outputs explicit

Current pipeline writes `frame.attributes`.

Refactor so that analyzers may write:

- scalar attributes into `frame.attributes`
- richer canonical outputs into `frame.metadata["canonical_outputs"]` or directly into `ScienceRunContext`

Recommendation:

- keep analyzers mostly unchanged where practical
- add an adapter layer in `SciencePipeline.process_image()` that extracts canonical outputs from analyzer metadata and persists them

#### 2.3 Affordance pipeline integration

Current state:

- affordance data is cached separately in `Image.meta_data`

Target:

- affordance becomes a first-class pipeline step when canonical processing runs
- its scores are persisted as scalar attributes and optionally stored as structured summary JSON
- its tag derivation happens at pipeline time

Implementation tasks:

- enhance `AffordanceAnalyzer` integration in `backend/science/pipeline.py`
- add scalar keys to the attribute registry
- define canonical thresholds for high/medium/low affordance tags
- persist raw scores to `Validation`
- persist tag rows to `science_tags`

Transitional compatibility:

- keep the existing affordance cache read path temporarily
- write new canonical outputs first
- later remove or de-emphasize `affordance_runtime_v1`

#### 2.4 Room-type pipeline integration

Current state:

- room detection is only a debug endpoint overlay

Target:

- room-type classification runs during canonical science processing
- top-k scores become canonical scalar attributes
- one primary room tag is emitted

Implementation tasks:

- extract room classifier logic from `v1_debug.py` into a reusable analyzer/service
- create a proper analyzer module under `backend/science/vision/` or `backend/science/semantics/`
- expose:
  - raw top-k class probabilities
  - chosen primary class
  - canonical tag creation

Do not leave room type as debug-only if it is product-significant.

#### 2.5 Segmentation/object pipeline integration

Current state:

- segmentation is optional in the pipeline
- debug overlays can compute segmentation on demand
- there is no canonical saved artifact contract

Target:

- segmentation runs in the canonical pipeline by default for current images targeted by Explorer processing
- default-threshold result is saved once
- scalar object summaries and tags are emitted

Implementation tasks:

- make segmentation part of the canonical Explorer science config
- persist one canonical segmentation artifact
- persist object summaries:
  - class count
  - class coverage ratio
  - present/absent
  - confidence aggregates if available
- emit canonical object tags from those summaries

Important:

- prefer saving reusable segmentation JSON plus one PNG
- render additional debug variants live from fresh computation or alternate params

#### 2.6 Canonical tag generation module

Create a dedicated tag derivation layer.

Suggested file:

- `backend/science/tag_derivation.py`

Responsibilities:

- generate tags from canonical attributes and summaries
- centralize thresholds and namespace rules
- remove tag-generation logic from `v1_discovery.py`

Example rules:

- `spatial.room_type.kitchen > 0.60` -> `room_type.kitchen`
- `segmentation.object.chair.present = 1` -> `object.chair`
- `affordance.L091 >= 5.5` -> `affordance.work.high`
- `style.minimalist >= 0.5` -> `style.minimalist`

### Exit criteria

- a single science run can persist:
  - scalar attributes
  - canonical tags
  - canonical segmentation artifact
  - structured summaries for affordance/room/objects


## Phase 3: Background scheduling and Explorer bootstrap

### Goals

- make science generation happen automatically as Explorer usage begins
- avoid blocking the UI

### Recommended trigger design

Do not interpret “as soon as the explorer starts up” as “browser must synchronously compute science.”

Instead:

1. Explorer app mounts
2. frontend calls a new endpoint:
   - `POST /v1/explorer/science/bootstrap`
3. backend:
   - determines active science version/config
   - finds images lacking a current completed run
   - enqueues them in background jobs
   - returns immediate summary

Example response:

```json
{
  "science_version": "3.4.74-canonical-explorer-v1",
  "queued_images": 412,
  "already_current": 9085,
  "running": 24,
  "failed": 3
}
```

### Reuse existing infrastructure

The repo already has lightweight asynchronous upload job infrastructure:

- `backend/services/upload_jobs.py`
- `backend/models/jobs.py`

Recommendation:

- generalize this into a broader science job executor rather than inventing a second scheduler

Options:

#### Option A: Extend existing upload job system

Pros:

- fastest path
- already aligned with background processing patterns

Cons:

- naming is awkward because the job concept is no longer only about uploads

#### Option B: Add `ScienceJob` / `ScienceJobItem`

Pros:

- cleaner semantics
- future-proof

Cons:

- more migration work

Recommendation:

- implement Phase 1 using the existing job machinery if speed matters
- rename/generalize later only if it becomes messy

### Concurrency model

Initial implementation:

- use FastAPI `BackgroundTasks` for kick-off only
- run actual worker logic in process with its own DB sessions

If throughput becomes a problem:

- promote to a dedicated worker process
- keep the service contract unchanged

### Scheduling policy

Bootstrap should:

- enqueue only missing or stale images
- respect a max queue size per bootstrap call
- avoid repeatedly enqueuing the same images
- mark stale outputs when science version/config changes

### Exit criteria

- first Explorer load triggers background backfill
- repeated Explorer loads do not duplicate work
- previously processed images are reused immediately


## Phase 4: API contract refactor

### Goals

- make Explorer read canonical outputs directly
- stop synthesizing canonical meaning in the API layer

### Endpoints to add or change

#### 1. `POST /v1/explorer/science/bootstrap`

Purpose:

- queue missing/stale science runs for Explorer-relevant images

#### 2. `GET /v1/explorer/science/status`

Purpose:

- lightweight progress/status for backlog and active version

Example fields:

- `science_version`
- `current_completed`
- `pending`
- `running`
- `failed`
- `last_bootstrap_at`

#### 3. Refactor `GET /v1/explorer/images/{image_id}/detail`

Current behavior:

- reads `Validation`
- assembles tags on the fly

Target behavior:

- fetch current `science_run`
- load canonical tags from `science_tags`
- load scalar attributes from `Validation`
- load artifact/summary metadata from `science_artifacts` and related storage
- include explicit run state

Recommended response additions:

- `science_run_status`
- `science_version`
- `science_is_current`
- `science_artifacts`
- `canonical_outputs_available`

#### 4. Refactor `POST /v1/explorer/search`

Target behavior:

- return imported tags plus canonical pipeline tags where available
- optionally expose `science_status` for each image card

### Compatibility strategy

Preserve current response fields initially:

- `tags`
- `science_attributes`
- `affordance_scores`

But change how they are populated:

- canonical stores first
- legacy cache fallback second

### Exit criteria

- Explorer reads canonical data rather than inferring it from mixed legacy sources


## Phase 5: Frontend changes

### Explorer app startup

File:

- `frontend/apps/explorer/src/App.jsx`

Tasks:

- on initial mount, call `POST /science/bootstrap`
- optionally poll `GET /science/status`
- show lightweight backlog progress if useful

Do not:

- block the initial image search on bootstrap completion

### Detail modal

File:

- `frontend/apps/explorer/src/ImageDetailModal.jsx`

Tasks:

1. Replace the misleading empty-state message.
2. Render run state explicitly.
3. Render canonical tags with clear provenance:
   - imported
   - pipeline
4. Expand `Science Attributes` to show grouped canonical outputs for:
   - existing science features
   - affordances
   - room type
   - segmentation/object summaries
5. Render canonical segmentation artifact if available for the default mode.

Recommended UX sections:

- `Tags`
- `Science Attributes`
- `Canonical Science Status`
- `Debug Views`

### Debug mode routing

Keep live mode behavior for:

- edges
- complexity
- depth
- alternate segmentation params

Recommended change:

- add a canonical segmentation/default view that loads the saved artifact first
- keep adjustable segmentation as a debug path

### Exit criteria

- UI distinction between canonical science outputs and debug outputs becomes obvious
- no more false suggestion that “nothing has been run” when canonical outputs exist


## Phase 6: Migration and backfill strategy

### Goals

- move to the new architecture without breaking current Explorer behavior

### Migration steps

#### Step 1

Add new tables and service layer without changing current endpoints.

#### Step 2

Teach the science pipeline to write to both:

- existing `Validation`
- new canonical stores

This is the safest intermediate state.

#### Step 3

Add bootstrap/status endpoints and wire Explorer startup.

#### Step 4

Update detail/search APIs to prefer canonical stores.

#### Step 5

Run a full backfill for existing images.

#### Step 6

After confidence is established:

- deprecate read-time tag synthesis in `v1_discovery.py`
- deprecate reliance on `Image.meta_data["affordance_runtime_v1"]` as canonical state

### Backfill strategy

Use batched execution:

- configurable batch size
- resumable runs
- idempotent by `science_version + config_fingerprint`

Recommended CLI:

- `backend/scripts/backfill_science_runs.py`

Capabilities:

- queue all missing images
- queue image id range
- queue upload batch
- re-run failed only
- mark stale and rebuild for a new science version


## Phase 7: Testing and verification

### Unit tests

Add tests for:

- science run deduplication
- canonical tag derivation logic
- affordance attribute persistence
- room-type attribute persistence
- segmentation summary extraction
- artifact registration and path creation

Suggested files:

- `tests/test_science_runs.py`
- `tests/test_tag_derivation.py`
- `tests/test_explorer_detail_canonical_outputs.py`

### Integration tests

Add tests covering:

1. Explorer bootstrap queues missing work
2. completed run populates detail endpoint
3. search returns canonical tags
4. unprocessed image returns accurate status
5. processed image returns both:
   - pipeline tags
   - matching science attributes

### Regression tests

Protect existing contracts:

- BN export still reads scalar science validations correctly
- monitor/tag inspector still works
- upload job processing still works

### Acceptance tests

For a representative image:

1. open Explorer
2. bootstrap is triggered
3. background science run completes
4. detail view shows:
   - room tag
   - object tags
   - affordance tags
   - corresponding scalar attributes
   - canonical segmentation artifact
5. debug views still work live for edges/complexity/depth


## Naming and Registry Plan

The shift will fail if naming is sloppy. Attribute keys and tags must be normalized before implementation.

### Recommended namespaces

#### Affordance

- `affordance.L059`
- `affordance.L079`
- `affordance.L091`
- `affordance.L130`
- `affordance.L141`

Optional aliases for UI only:

- `affordance.sleep`
- `affordance.cook`
- `affordance.work`

#### Room type

- `spatial.room_type.kitchen`
- `spatial.room_type.bedroom`
- `spatial.room_type.living_room`
- `spatial.room_type.home_office`

Tag namespace:

- `room_type.kitchen`

#### Objects

- `segmentation.object.chair.present`
- `segmentation.object.chair.count`
- `segmentation.object.chair.coverage_ratio`

Tag namespace:

- `object.chair`

### Registry requirement

Every persisted `Validation.attribute_key` must exist in the attribute registry before rollout.

This means the plan must include updates to:

- attribute seeds
- feature registry
- governance checks if any rely on coverage


## Risks and Mitigations

### Risk 1: Explorer startup triggers too much work

Problem:

- first load might enqueue the entire corpus

Mitigation:

- bootstrap in bounded batches
- throttle queueing
- expose progress and continuation
- optionally prefer recently viewed / search-returned images first

### Risk 2: In-process background execution is fragile

Problem:

- web process restarts may interrupt long runs

Mitigation:

- science runs must be resumable and status-driven
- failed/running stale jobs should be recoverable on next bootstrap
- consider a dedicated worker in a later phase

### Risk 3: Registry drift blocks persistence

Problem:

- new affordance/room/object keys may violate FK constraints on `validations.attribute_key`

Mitigation:

- add registry updates before enabling writes
- add migration/test coverage

### Risk 4: Object tag explosion

Problem:

- segmentation may produce too many low-value object tags

Mitigation:

- apply canonical thresholds
- only emit tags for classes above minimum area/presence/confidence
- keep richer object detail in `science_attributes`, not all as tags

### Risk 5: Re-running versions creates duplicate ambiguous outputs

Problem:

- multiple science versions may coexist

Mitigation:

- `science_runs.is_current`
- version/config fingerprinting
- API reads only current run unless explicitly asked otherwise

### Risk 6: Segmentation artifact format is chosen poorly

Problem:

- storing only a PNG may not be enough for future reuse

Mitigation:

- save both:
  - one PNG artifact
  - one machine-readable JSON summary


## Recommended Implementation Order

This is the safest sequence.

1. Finalize canonical naming and thresholds.
2. Add new persistence tables and migration.
3. Add `science_runs` service layer and bootstrap/status endpoints.
4. Refactor pipeline to write canonical outputs for:
   - affordance
   - room type
   - segmentation/object summaries
5. Persist canonical tags in `science_tags`.
6. Save canonical segmentation artifact.
7. Update detail endpoint to read canonical stores.
8. Update Explorer UI states and messaging.
9. Update search endpoint to include canonical tags.
10. Backfill the corpus.
11. Remove or downgrade legacy read-time tag synthesis.


## Concrete File Touch Map

Expected primary implementation files:

- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/backend/science/pipeline.py`
- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/backend/api/v1_discovery.py`
- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/backend/api/v1_debug.py`
- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/backend/main.py`
- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/backend/services/upload_jobs.py`
- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/backend/models/assets.py`
- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/backend/models/annotation.py`
- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/frontend/apps/explorer/src/App.jsx`
- `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/frontend/apps/explorer/src/ImageDetailModal.jsx`

Expected new files:

- `backend/models/science_runs.py`
- `backend/services/science_runs.py`
- `backend/science/run_context.py`
- `backend/science/tag_derivation.py`
- `backend/scripts/backfill_science_runs.py`
- `tests/test_science_runs.py`
- `tests/test_tag_derivation.py`
- `tests/test_explorer_detail_canonical_outputs.py`

Expected registry/contract updates:

- `backend/science/features_registry.py`
- `backend/science/features_canonical.jsonl`
- `contracts/attributes.yml`
- `backend/data/goldilocks_attributes.csv`
- `docs/SCIENCE_TAG_MAP.md`


## Non-Goals for This Shift

To keep the change tractable, this plan does not require in Phase 1:

- saving every debug PNG artifact
- saving alternate-threshold edge maps
- saving alternate-threshold segmentation overlays
- fully replacing all debug endpoints with artifact-serving endpoints
- redesigning the entire Monitor or Admin app
- introducing Celery/RQ/Kafka immediately


## Definition of Done

The architectural shift is complete when all of the following are true:

1. Explorer startup triggers backend scheduling for missing canonical science runs.
2. Previously processed images are reused without re-running science.
3. Affordance, room type, and segmentation/object results are part of the canonical science pipeline.
4. Every pipeline-derived tag shown in Explorer comes from persisted canonical output.
5. The `Science Attributes` panel shows the underlying persisted scalar values for those outputs.
6. A canonical segmentation artifact is saved and reused.
7. Debug-only parameterized modes still work live on demand.
8. The empty states and status labels in the UI are truthful.
9. Existing BN and supervision flows continue to function.


## Recommended First Milestone

If this work is split into milestones, the first milestone should be:

### Milestone 1: Canonical Run Tracking + Affordance/Room/Object Persistence

Scope:

- add `science_runs`, `science_tags`, `science_artifacts`
- bootstrap endpoint
- pipeline writes current scalar outputs plus:
  - affordance scalar values and tags
  - room scalar values and tag
  - segmentation object summaries and tags
- save one canonical segmentation artifact
- detail endpoint reads canonical stores
- UI copy becomes truthful

This milestone delivers the architectural foundation and resolves the current conceptual mismatch without requiring a full debug-system rewrite.
