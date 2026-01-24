# Image Analyzer System: Data Structure Revision and Integration Plan

## Executive Summary

This plan defines the data structure revisions and cross-module
expectations needed to align the Image Analyzer workspace with the
taxonomy, tagging, and statistical updates in:

- `tagging-update-docs/Rules_Classification_and_Interactions_v1.xlsx`
- `tagging-update-docs/Environment_Cognition_Taxonomy_Hierarchical_V2.7_ActivityAffordances_RoomMarkers copy.xlsx`
- `tagging-update-docs/tag detection ideas.md`
- `stats-update-docs/statistics_methods_description.md`
- `stats-update-docs/uncertainty_update_guide.md`

The core objective is to establish a shared, versioned data contract
across Article Eater, Image Tagger, Knowledge Graph UI, and Graphical
Model. The revised contract will represent:

- Hierarchical taxonomies for attributes, latents, mediators, outcomes.
- Marker nodes (building typology, room type) and activity affordances.
- Rule and evidence structures that encode uncertainty classes
  (pi, gamma, tau^2, sigma^2, phi, kappa/GRADE).
- Detection confidence and extractability tiers derived from visual
  evidence limitations.

This plan is an architectural and data integration roadmap. It does not
implement code changes. Implementation should follow this plan as the
source of truth.

---

## Current State and Gaps

### Current Data Structure Mismatch

1. **Image Tagger**
   - Outputs visual attributes and tags but does not use the new
     hierarchical taxonomy IDs (e.g., V1-xxx, Lxx, Mxx).
   - Lacks explicit confidence classes for detectable vs inferred tags.
   - Does not encode marker nodes or activity affordances.

2. **Article Eater**
   - BN export schema provides nodes/edges but does not carry the new
     uncertainty classes (pi, gamma, tau^2, sigma^2, phi, kappa).
   - Rules are not normalized to the updated antecedent/consequent
     taxonomy paths defined in the new hierarchy sheets.

3. **Knowledge Graph UI**
   - Demo-only in-memory graph with no taxonomy alignment.
   - No representation of uncertainty classes, evidence tier, or GRADE.

4. **Graphical Model**
   - Uses the three-layer structure but lacks explicit mapping to the
     hierarchical attribute DAG and updated mediator/outcome taxonomy.
   - Uncertainty is currently modeled as posterior distributions but is
     not segmented into structural, causal, heterogeneity, parametric,
     and specification uncertainty classes.

### Target Outcome

A unified data model that:

- Supports hierarchical attribute DAGs (computed vs exogenous).
- Treats mediators as measured constructs with indicator mappings.
- Encodes uncertainty classes per edge and per inference step.
- Formalizes activity affordances and marker nodes as moderator priors.

---

## Target Data Model (Unified Contract v0.1)

### Core Entities

1. **Marker Nodes**
   - Building typology (e.g., BT01 Residential)
   - Room type (e.g., RT02 Living Room / Lounge)
   - Purpose: prior context and moderation for activities and rules.

2. **Environmental Attributes**
   - IDs: V1-xxx (from Env_Attributes sheet).
   - Fields: domain, subdomain, extractability, evidence strength.
   - Distinguish exogenous vs computed attributes (hierarchical DAG).

3. **Latent Variables**
   - IDs: Lxx (from Latent_Variables sheet).
   - Fields: observable cues, indicators, judgability, tier.

4. **Mediators**
   - IDs: Mxx (from Mediators sheet).
   - Fields: definition, cues, recommended measures.

5. **Outcomes**
   - Outcome constructs and measurement instruments.

6. **Activity Affordances**
   - IDs: L0xx activity latents with RoomType priors.
   - Fields: family, cues, strength priors.

7. **Rules and Interactions**
   - Antecedent/Consequent paths from Rules_Classification sheet.
   - Support multiple antecedents and interactions.

### Uncertainty Classes (Edge and Rule Level)

All rules and causal edges must include:

- **pi**: Structural probability (edge exists).
- **gamma**: Causal identification probability.
- **tau2**: Between-study heterogeneity.
- **sigma2**: Parametric uncertainty (sampling variance).
- **phi**: Functional form correctness (model specification).
- **kappa**: GRADE-style evidence certainty class.

These align with `stats-update-docs/uncertainty_update_guide.md`.

### Detection Confidence (Tag/Attribute Level)

Each detected tag or attribute must include:

- **detection_class**: detected | computed | inferred | proxy_only.
- **extractability**: 2d_high | 2d_partial | 3d_partial | sensor_only.
- **confidence_gamma**: approximate reliability class
  (0.80-0.85 high, 0.60-0.75 medium, 0.40-0.65 low).
- **method**: detector/algorithm (e.g., Places365, segmentation, depth).

These align with `tagging-update-docs/tag detection ideas.md`.

---

## Module Revisions and Expectations

### 1. Image Tagger (Tag/Attribute Producer)

**Primary role:** Produce observable attributes, marker nodes, and
activity affordance priors.

**Required data changes:**

- Map all attribute outputs to `Env_Attributes` IDs and names.
- Output marker nodes (BuildingTypology, RoomType) for each image.
- Output activity affordance priors using RoomType_to_Activity mapping.
- Tag each output with detection_class, extractability, confidence_gamma.
- Distinguish:
  - **Detected**: room type, objects, materials, lighting (high).
  - **Computed**: complexity, entropy, prospect/refuge (medium).
  - **Inferred**: psychological latents (low, explicit uncertainty).
  - **Proxy-only**: acoustic/thermal/olfactory (very low).

**Data expectations:**

```
image_id
  marker_nodes: [BTxx, RTxx]
  attributes: [
    { attribute_id: V1-001, value: 320, detection_class: "computed",
      extractability: "2d_partial", confidence_gamma: 0.65 }
  ]
  activity_affordances: [
    { activity_id: L060, prior: 0.75, basis: "RoomType" }
  ]
```

### 2. Article Eater (Evidence and Rule Producer)

**Primary role:** Produce evidence-backed rules with taxonomy-aligned
antecedents and consequents.

**Required data changes:**

- Normalize rules to antecedent/consequent paths in
  `Rules_Classification_and_Interactions_v1.xlsx`.
- For each rule edge, populate uncertainty classes: pi, gamma, tau2,
  sigma2, phi, kappa.
- Emit evidence tier classification (Tier 1/2/3 study types).
- Preserve existing BN export but add:
  - `evidence_quality` (kappa).
  - `uncertainty` block with pi/gamma/tau2/sigma2/phi.

**Rule edge schema extension (BN export):**

```
{
  "edge_id": "ARCv4_5_000002",
  "antecedent_path": "Acoustics > Speech Privacy > STI (index)",
  "consequent_path": "Social/Interpersonal > Communication Quality > ...",
  "direction": "decreases",
  "polarity": "negative",
  "uncertainty": {
    "pi": 0.70, "gamma": 0.35, "tau2": 0.08, "sigma2": 0.04, "phi": 0.80
  },
  "kappa": "C",
  "evidence_tier": "Tier3_CrossSectional"
}
```

### 3. Knowledge Graph UI (Evidence Graph Consumer)

**Primary role:** Visualize evidence with uncertainty and taxonomy.

**Required data changes:**

- Replace demo graph with taxonomy-aligned graph nodes:
  - Markers (BTxx, RTxx) and attributes (V1-xxx).
  - Latents (Lxx) and mediators (Mxx).
  - Outcomes with measurement references.
- Display uncertainty classes per edge:
  - pi/gamma/tau2/sigma2/phi/kappa.
- Provide filtering by:
  - evidence tier, kappa, detection_class, extractability.

**UI expectations:**

- Edges show a compact "uncertainty badge" (pi/gamma/phi/kappa).
- Node panels show extractability and measurement methods.
- Filtering toggles for detected vs inferred vs proxy-only attributes.

### 4. Graphical Model (Causal Inference Engine)

**Primary role:** Use hierarchy-aware attributes and uncertainty classes
to generate predictions with honest uncertainty.

**Required data changes:**

- Incorporate attribute DAG (exogenous vs computed attributes).
- Accept marker nodes and activity affordances as priors/moderators.
- Propagate uncertainty via:
  - structural (pi), causal (gamma), heterogeneity (tau2),
  - parametric (sigma2), functional form (phi).
- Implement model specification selection for Goldilocks attributes:
  - phi controls the probability of using correct functional form.

**Prediction output expectations:**

```
outcome: stress_level
  mean: 4.1
  ci_95: [3.3, 5.0]
  uncertainty_breakdown:
    pi: 0.10
    gamma: 0.20
    tau2: 0.25
    sigma2: 0.15
    phi: 0.10
```

---

## Revised Data Flow (Target State)

```mermaid
flowchart LR
    AE[Article Eater\nRules + Evidence\n(pi,gamma,tau2,sigma2,phi,kappa)]
    IT[Image Tagger\nMarkers + Attributes\n(detection_class, extractability)]
    KG[Knowledge Graph\nTaxonomy + Evidence Graph]
    GM[Graphical Model\nHierarchical Causal Inference]

    AE --> KG
    IT --> GM
    KG --> GM
    GM --> KG
```

---

## Phased Implementation Plan

### Phase 0: Contract Definition and Versioning

**Goal:** Publish shared data contract v0.1.

Steps:
1. Define canonical IDs for Marker, Attribute, Latent, Mediator, Outcome.
2. Define rule/edge schema with uncertainty classes.
3. Publish JSON schema files in `contracts/` (new).
4. Update BN export schema in Article Eater to include uncertainty fields.

Deliverables:
- `contracts/marker_nodes.schema.json`
- `contracts/env_attributes.schema.json`
- `contracts/latents.schema.json`
- `contracts/mediators.schema.json`
- `contracts/edges.schema.json`

### Phase 1: Image Tagger Alignment

**Goal:** Ensure image tagging outputs conform to taxonomy IDs and
confidence classes.

Steps:
1. Map tagger outputs to `Env_Attributes` IDs and domains.
2. Add marker node classifiers (BTxx, RTxx).
3. Add activity affordance priors per RoomType.
4. Add detection_class and extractability metadata.

Deliverables:
- New API payloads for tag outputs.
- Tag metadata fields for confidence and extractability.

### Phase 2: Article Eater Alignment

**Goal:** Normalize rules to taxonomy paths and add uncertainty classes.

Steps:
1. Map antecedent/consequent to Rule taxonomy paths.
2. Add uncertainty and GRADE metadata to BN export.
3. Add evidence tier classification to each rule.

Deliverables:
- Updated BN export schema and examples.
- Rule validation tool to check taxonomy alignment.

### Phase 3: Knowledge Graph Upgrade

**Goal:** Load taxonomy-aligned graph and display uncertainty.

Steps:
1. Replace in-memory nodes/edges with taxonomy-aligned dataset.
2. Add uncertainty and evidence class display in the UI.
3. Add filters by evidence tier, kappa, detection_class.

Deliverables:
- New backend loader for taxonomy-based graph.
- UI updates for uncertainty visualization.

### Phase 4: Graphical Model Integration

**Goal:** Use updated attributes and uncertainty to drive inference.

Steps:
1. Introduce attribute DAG (exogenous vs computed).
2. Add uncertainty classes to edge priors.
3. Implement Monte Carlo propagation across uncertainty dimensions.
4. Add uncertainty breakdown to prediction results.

Deliverables:
- Updated statistical engine interfaces.
- Prediction outputs with uncertainty decomposition.

### Phase 5: End-to-End Validation

**Goal:** Verify data contract conformance and pipeline flow.

Steps:
1. Create synthetic test fixtures aligned to new taxonomy.
2. Validate BN exports against contract schemas.
3. Run integration tests across modules.
4. Document compliance in an integration audit.

Deliverables:
- Integration tests in `integration/`.
- Audit report for contract conformance.

---

## Migration Notes and Compatibility

- Existing outputs should continue to work during a deprecation window.
- Provide a translation layer for:
  - legacy attribute names -> V1-xxx IDs
  - legacy mediator names -> Mxx IDs
  - legacy outcome labels -> Outcome_Measures.
- Implement a version field in all module payloads.

---

## Risks and Mitigations

1. **Taxonomy Drift**
   - Mitigation: Centralize IDs and provide a schema validator.

2. **Incomplete Extractability**
   - Mitigation: Encode detection_class and confidence_gamma explicitly;
     avoid false precision in predictions.

3. **Uncertainty Misinterpretation**
   - Mitigation: Provide UI tooltips and API docs for pi/gamma/tau2/etc.

4. **Overloaded Models**
   - Mitigation: Use hierarchical modeling and composite attributes
     where correlations are high.

---

## Out of Scope (This Plan)

- Implementation details for each module.
- Frontend redesign beyond uncertainty display.
- New data collection or experiments (covered in stats roadmap).

---

## Success Criteria

The integration is complete when:

1. All modules emit/consume taxonomy-aligned IDs.
2. Rules and edges include full uncertainty classes.
3. Tag outputs include detection_class and extractability metadata.
4. Knowledge Graph UI displays evidence quality and uncertainty.
5. Graphical Model predictions include uncertainty breakdowns.

