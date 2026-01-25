# Adaptive Preference Testing System (GUI + Backend) — Repository Documentation

**Package:** `COMPLETE_v3.5.11_SYSTEM` 
**Date (doc generated):** 
**What’s in this repo:** A complete end‑to‑end system for running *pairwise* adaptive preference experiments (stimulus A vs stimulus B), including:
- A Flask + PostgreSQL backend API
- A “pure” Bayesian adaptive pair-selection engine
- Multiple static HTML/JS GUIs (experimenter, admin, subject, results)
- SQL schema, tests, and a governance/installer toolchain

> Note: This archive also contains a prebuilt `.venv` folder and a `.git` folder. Those are not required for understanding the system; they inflate file counts. The “core system” is ~41 files / ~580 KB (excluding `.venv`, `.git`, uploads, caches).

---

## 1) What it is

An **Adaptive Preference Testing** platform that learns a participant’s latent preference ranking over a set of stimuli by:
1) showing **two stimuli at a time** (paired comparison),
2) recording the participant’s choice,
3) using a Bayesian model to update beliefs,
4) selecting the *next* pair to maximize expected learning (information gain),
5) producing ranked outcomes + analysis exports.

This is ideal for experiments where absolute rating scales are noisy, but **comparative judgments** (“A or B?”) are reliable.

---

## 2) What it does (capabilities)

### Experimenter / Researcher
- Create and configure an experiment (name, instructions, trial limits, algorithm hyperparameters).
- Upload stimuli (images) and associate them with experiments.
- Publish experiments and obtain a subject URL (subject interface loads by experiment/session token).
- Monitor results and export data as CSV.

### Participant / Subject
- Consent → repeated pairwise choices → debrief.
- Progress indicators, break logic, and network-resilience features (queueing + retry) are implemented on the subject UI.

### Admin
- Manage consent/debrief documents.
- View all experiments and run exports (depending on role).

---

## 3) How it works (principles + algorithm)

### 3.1 The core mathematical idea
The backend maintains a **Bayesian belief** over each stimulus’ “utility” (latent preference score).

- Let each stimulus have a latent utility \(u_i\).
- The system maintains a Gaussian belief:
 - Mean vector **μ**: current best estimate of utilities
 - Covariance **Σ**: uncertainty and correlations between utilities

When the participant chooses between stimulus *i* and *j*, the model uses a **Bradley–Terry / probit-like** likelihood to update μ and Σ.

### 3.2 Pair selection strategy (adaptive)
For every candidate pair (i, j), the selector computes an **expected information gain** proxy:

- If the model believes the outcome is uncertain (probability near 0.5) **and** uncertainty is high, the pair is highly informative.
- An optional exploration bonus favors pairs that have been compared less often.

Then it picks the pair with the maximum score.

**Where implemented:**
- `backend/bayesian_adaptive.py`
 - `BayesianPreferenceState` stores μ, Σ, and a comparison matrix.
 - `PureBayesianAdaptiveSelector.select_next_pair` chooses the next pair.
 - `PureBayesianAdaptiveSelector.update_beliefs` updates μ, Σ after a choice.
 - `check_convergence` can stop early when uncertainty is low.

---

## 4) System architecture (big picture)

```mermaid
flowchart LR
 subgraph Frontend (static HTML/JS)
 E[Experimenter Dashboard] -->|REST| API
 A[Admin Dashboard] -->|REST| API
 S[Subject Interface] -->|REST| API
 R[Results Dashboard] -->|REST| API
 end

 subgraph Backend (Flask)
 API[backend/api.py]
 ALG[backend/bayesian_adaptive.py]
 AUTH[backend/auth.py]
 API --> ALG
 API --> AUTH
 end

 subgraph Database (PostgreSQL)
 DB[(schema.sql tables)]
 end

 API -->|SQLAlchemy| DB
 API -->|serves /uploads| U[(uploads/ images)]
```

### Key data flow
- GUIs call `http://localhost:5000/api/...` endpoints.
- Backend stores experiment config, sessions, algorithm state, and choices in PostgreSQL.
- Uploaded images are stored in `backend/uploads/` and served at `/uploads/<filename>`.

---

## 5) Simple step‑through (inputs → outputs)

### 5.1 Experiment creation (researcher)
**Input:** experiment configuration + stimuli uploads 
**Process:**
1. Experimenter opens `frontend/experimenter_dashboard_improved.html`.
2. UI calls `POST /api/experiments` with config.
3. UI uploads images to `POST /api/stimuli/upload`.
4. UI associates stimuli with an experiment via `PATCH /api/stimuli/<id>/assign_experiment` (or experiment-specific stimulus endpoints).
5. Researcher publishes via `POST /api/experiments/<experiment_id>/publish`.

**Output:** a published experiment in DB + images in uploads folder + a subject URL token flow.

### 5.2 Starting a participant session
**Input:** experiment_id + subject/session metadata (participant id, ip, etc.) 
**Process:**
1. Subject opens `frontend/subject_interface_complete.html?exp=<experiment_id>` (exact parameter handling depends on the UI build).
2. UI calls `POST /api/sessions` to create a session token.
3. Backend initializes algorithm state in `algorithm_state` table.

**Output:** `session_token` + initialized Bayesian state (μ, Σ).

### 5.3 Running trials (the adaptive loop)
For each trial t = 1..T:

1. **Next pair request** 
 UI calls: `GET /api/sessions/<session_token>/next` 
 Backend:
 - loads current Bayesian state
 - calls `select_next_pair`
 - returns (stimulus A, stimulus B) + a **pair_token** JWT encoding session_id + trial + the shown pair

2. **Choice submission** 
 UI calls: `POST /api/sessions/<session_token>/choice` with:
 - which stimulus was chosen
 - the **pair_token** to prove the choice corresponds to the shown pair 
 Backend:
 - validates the pair_token (prevents mismatch / replay)
 - updates Bayesian state via `update_beliefs`
 - stores the choice row in `choices`

**Output:** growing choice dataset + refined μ/Σ. 

### 5.4 Results + export
**Input:** experiment_id 
**Process:** Results dashboard calls:
- `GET /api/experiments/<experiment_id>/results`
- `GET /api/experiments/<experiment_id>/export_choices_csv`
- `GET /api/experiments/<experiment_id>/export_clean_choices_csv`

**Output:** on-screen analytics + downloadable CSV.

---

## 6) The GUIs (what they are + how they map to APIs)

### 6.1 Experimenter Dashboard
**File:** `frontend/experimenter_dashboard_improved.html` 
**Purpose:** create/edit experiments, manage stimuli, publish, and navigate to results/admin.

**Typical API calls:**
- `GET /api/experiments/all` (or scoped list in some builds)
- `POST /api/experiments`
- `PUT /api/experiments/<experiment_id>`
- `POST /api/stimuli/upload`
- `GET /api/stimuli`
- `PATCH /api/stimuli/<stimulus_id>/assign_experiment`
- `POST /api/experiments/<experiment_id>/publish`

### 6.2 Subject Interface
**File:** `frontend/subject_interface_complete.html` 
**Purpose:** consent → pairwise trials → debrief. 
Includes robustness features like retry/backoff, offline banner, and queued requests (as described in README).

**Typical API calls:**
- `POST /api/sessions`
- `GET /api/sessions/<session_token>/next`
- `POST /api/sessions/<session_token>/choice`
- `GET /api/consent`
- `GET /api/debrief`

### 6.3 Admin Dashboard
**File:** `frontend/admin_PATCHED.html` 
**Purpose:** admin operations, bulk views, doc uploads, shortcuts.

**Typical API calls:**
- `POST /api/admin/upload_consent`
- `POST /api/admin/upload_debrief`
- `GET /api/experiments/all`

### 6.4 Results Dashboard
**File:** `frontend/results_dashboard.html` 
**Purpose:** show results for a selected experiment + export CSV.

**Typical API calls:**
- `GET /api/experiments/<experiment_id>/results`
- `GET /api/experiments/<experiment_id>/export_choices_csv`
- `GET /api/experiments/<experiment_id>/export_clean_choices_csv`

---

## 7) Database: tables and what they store

**Schema file:** `database/schema.sql`

### Core tables
- `users` — researcher accounts and roles
- `experiments` — experiment definitions and algorithm parameters
- `stimuli` — stimulus metadata and file references
- `sessions` — per-subject sessions (tokens, timing, status)
- `algorithm_state` — serialized Bayesian state per session (μ, Σ, comparison matrix)
- `choices` — every pairwise decision record
- `audit_log` — security/trace events
- `provenance_log` — data lineage and export provenance
- `schema_version` — schema migration/version marker

---

## 8) Backend API overview (important endpoints)

**Server:** `backend/api.py` 
**Base path:** `/api`

### Stimuli
- `GET /api/stimuli` — list stimuli (optionally filtered)
- `POST /api/stimuli/upload` — upload an image file to `backend/uploads/`
- `PUT /api/stimuli/<stimulus_id>` — update stimulus metadata
- `POST /api/stimuli/<stimulus_id>/auto_tag` — auto-tagging hook (implementation-specific)
- `PATCH /api/stimuli/<stimulus_id>/assign_experiment` — attach to experiment

### Experiments
- `POST /api/experiments` — create
- `GET /api/experiments/<experiment_id>` — read
- `PUT /api/experiments/<experiment_id>` — update
- `POST /api/experiments/<experiment_id>/stimuli` — add stimuli linkage
- `POST /api/experiments/<experiment_id>/publish` — publish
- `POST /api/experiments/<experiment_id>/archive` — archive
- `DELETE /api/experiments/<experiment_id>` — delete
- `GET /api/experiments/all` — list (often used by admin/results)

### Sessions (subject run)
- `POST /api/sessions` — create a new subject session
- `GET /api/sessions/<session_token>/next` — get next adaptive pair + pair_token
- `POST /api/sessions/<session_token>/choice` — submit choice + pair_token

### Results / exports
- `GET /api/experiments/<experiment_id>/results`
- `GET /api/experiments/<experiment_id>/export_choices_csv`
- `GET /api/experiments/<experiment_id>/export_clean_choices_csv`

### Consent / debrief content
- `GET /api/consent`
- `GET /api/debrief`
- `POST /api/admin/upload_consent`
- `POST /api/admin/upload_debrief`

### Health
- `GET /api/health`

---

## 9) Authentication & “pair_token/session mismatch”

**Auth module:** `backend/auth.py`

Two concepts exist in this system:

### 9.1 Researcher/admin auth
`require_auth` + `require_roles` support Bearer JWTs issued with `ADAPTIVE_PREF_JWT_SECRET`. 
There is also a dev helper endpoint:
- `POST /api/auth/dev_issue_token` — issues a token (for local development).

### 9.2 Pair-token for trial integrity
Every time the subject asks for the **next pair**, the backend issues a short JWT (“pair_token”) that encodes:
- session_id
- trial_number
- stimulus_a_id / stimulus_b_id
- presentation_order

When the subject submits a choice, the backend verifies that the pair_token matches the session/trial. 
If you ever see **“pair_token/session mismatch”**, it usually means:
- the frontend submitted a choice from an *older* displayed pair (race condition),
- the user refreshed mid-trial and the UI re-used stale localStorage,
- multiple tabs were open for the same session,
- or the backend session token changed (new session created) but the old pair_token was reused.

---

## 10) Key scripts and “minimum functions” to understand

### 10.1 Installer
- `install.sh` 
Creates a `.venv`, installs requirements, then runs governance checks.

### 10.2 Governance / guard scripts (defensive tooling)
Located in `scripts/`:
- `hollow_repo_guard.py` — checks for missing expected directories/files
- `program_integrity_guard.py` — validates important program invariants
- `syntax_guard.py` — syntax checks on key Python/HTML assets
- `critical_import_guard.py` — verifies critical imports don’t break
- `canon_guard.py` — checks the “canonical” file set described by governance manifests
- `guardian.py` / `rot_audit_prompt.py` — repo health / “rot” detection helpers

### 10.3 Core algorithm objects (minimum to understand the math)
- `BayesianPreferenceState`
 - `mu` (means), `Sigma` (covariance), `comparison_matrix`
 - serialization helpers `to_dict` / `from_dict`
- `PureBayesianAdaptiveSelector`
 - `select_next_pair(state)` — which two stimuli to show next
 - `update_beliefs(state, i, j, winner)` — update posterior approximation after a choice
 - `_expected_information_gain(i, j, state)` — scoring function used for selection
 - `check_convergence(state, threshold)` — stop condition

### 10.4 Core backend functions (minimum to understand the pipeline)
- Session creation (`POST /api/sessions`)
- Pair issuance (`GET /api/sessions/<token>/next`)
- Choice submission (`POST /api/sessions/<token>/choice`)
- Results aggregation/export endpoints

---

## 11) How to run locally (short, practical)

### 11.1 Database
Create and load schema:
```bash
createdb adaptive_preference
psql -d adaptive_preference -f database/schema.sql
```

Set environment:
```bash
export DATABASE_URL="postgresql://localhost/adaptive_preference"
export SECRET_KEY="dev-secret"
export ADAPTIVE_PREF_JWT_SECRET="dev-jwt-secret"
```

### 11.2 Backend
```bash
python backend/api.py
# http://localhost:5000
```

### 11.3 Frontend
Open these in a browser (they are static files):
- `frontend/experimenter_dashboard_improved.html`
- `frontend/admin_PATCHED.html`
- `frontend/results_dashboard.html`
- `frontend/subject_interface_complete.html?demo=true`

---

## 13) Where to look next (quick “map”)

- **Backend core:** `backend/api.py`
- **Bayesian algorithm:** `backend/bayesian_adaptive.py`
- **Auth + pair tokens:** `backend/auth.py`
- **DB structure:** `database/schema.sql`
- **GUIs:** `frontend/*.html`
- **Governance/installer:** `install.sh`, `v3_governance.yml`, `scripts/*.py`

---

## Appendix A — File inventory (core)

```
backend/
 api.py
 bayesian_adaptive.py
 auth.py
database/
 schema.sql
frontend/
 experimenter_dashboard_improved.html
 stimulus_library.html
 subject_interface_complete.html
 results_dashboard.html
 admin_PATCHED.html
tests/
 conftest.py
 test_consent_endpoint.py
 test_csv_contract.py
```
