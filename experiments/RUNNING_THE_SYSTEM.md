# RUNNING_THE_SYSTEM.md
### First-Time Setup & Onboarding Guide for the Adaptive Preference Testing System

This guide explains exactly how to run the full system locally for the first time, including:

- Backend (Flask API)
- Frontend (HTML/JS GUI)
- PostgreSQL database setup
- Dev Login workflow
- Environment variables
- Avoiding the file-system mistakes that break the repo

It is written for Mac (Intel/Apple Silicon) and Linux, but Windows WSL also works.

---

# 🔷 QUICK START (TL;DR)

If you already have PostgreSQL installed and running, the minimum steps are:

```bash
cd Adaptive_Preference_GUI/Adaptive_Preference\ _3.5.11_Handoff\ /COMPLETE_v3.5.11_SYSTEM

rm -rf backend/venv     # remove the broken included venv
chmod +x install.sh
./install.sh            # sets up new .venv and installs requirements

nano backend/.env       # ensure DATABASE_URL matches your system
createdb adaptive_testing

source .venv/bin/activate
export $(grep -v '^#' backend/.env | xargs)
psql "$DATABASE_URL" -f database/schema.sql

python backend/api.py   # start backend
```

Then in another terminal:

```bash
cd frontend
python -m http.server 8000
```

Then in browser:

1. Open `http://localhost:8000/admin_PATCHED.html`
2. Click **Dev Login (researcher)**
3. Navigate to Experimenter Dashboard, Stimulus Library, etc.

---

# 1. OVERVIEW OF THE SYSTEM

```
COMPLETE_v3.5.11_SYSTEM/
│
├── backend/          # Python API (Flask)
│   ├── api.py
│   ├── auth.py
│   ├── bayesian_adaptive.py
│   ├── .env          <-- your local environment file
│   └── (DELETE THIS IF YOU SEE IT) venv/
│
├── frontend/         # HTML/JS GUIs
│   ├── admin_PATCHED.html
│   ├── experimenter_dashboard_improved.html
│   ├── stimulus_library.html
│   ├── results_dashboard.html
│   ├── subject_interface_complete.html
│   └── docs/
│
├── database/
│   └── schema.sql    # PostgreSQL definition
│
├── scripts/          # Governance, integrity guards
│   └── ...py
│
├── install.sh        # Sets up .venv & installs all requirements
├── requirements.txt
└── v3_governance.yml
```

The backend expects this structure exactly.
Do NOT move or flatten folders.

---

# 2. REQUIREMENTS

### ✔ Python 3.9 – 3.12
### ✔ PostgreSQL 14+
### ✔ A terminal and basic shell commands

---

# 3. PREPARE THE PROJECT

Navigate to the repo root:

```bash
cd Adaptive_Preference_GUI/Adaptive_Preference\ _3.5.11_Handoff\ /COMPLETE_v3.5.11_SYSTEM
```

---

# 4. REMOVE THE OLD INCLUDED VENV

The zip you received includes a pre-built `backend/venv` from someone else’s machine.
This will always break things.

Remove it:

```bash
rm -rf backend/venv
```

---

# 5. RUN THE INSTALLER (CREATES A NEW .venv)

```bash
chmod +x install.sh
./install.sh
```

This creates:

```
COMPLETE_v3.5.11_SYSTEM/.venv
```

and installs all dependencies.

---

# 6. CONFIGURE THE BACKEND ENVIRONMENT

Open:

```bash
nano backend/.env
```

You will see something like:

```env
DATABASE_URL=postgresql://postgres@localhost/adaptive_testing
SECRET_KEY=flask-secret-key-change-in-production-67890
ADAPTIVE_PREF_JWT_SECRET=CHANGE_THIS_IN_PRODUCTION_TO_RANDOM_STRING_12345
AUTH_DEV_ISSUE_TOKENS=1
ALLOWED_ORIGINS=http://localhost:8000
```

## Most Important Line: DATABASE_URL

It must match a real database on your machine.

If using the default:

```bash
createdb adaptive_testing
```

If your PostgreSQL user is your mac username:

```env
DATABASE_URL=postgresql://<your_mac_username>@localhost/adaptive_testing
```

Save file & exit.

---

# 7. LOAD THE DATABASE SCHEMA

Activate environment:

```bash
source .venv/bin/activate
```

Load env vars:

```bash
set -a
source backend/.env
set +a
```

Load schema:

```bash
psql "$DATABASE_URL" -f database/schema.sql
```

This creates tables:

- experiments
- stimuli
- sessions
- choices
- algorithm_state
- audit_log
- provenance_log

---

# 8. START THE BACKEND API

```bash
source .venv/bin/activate
set -a; source backend/.env; set +a
python backend/api.py
```

You should see:

```
* Running on http://127.0.0.1:5000
```

---

# 9. START THE FRONTEND (STATIC SERVER)

In a new terminal:

```bash
cd Adaptive_Preference_GUI/Adaptive_Preference\ _3.5.11_Handoff\ /COMPLETE_v3.5.11_SYSTEM/frontend
python -m http.server 8000
```

Then open in browser:

```
http://localhost:8000/admin_PATCHED.html
```

---

# 10. FIRST-RUN WORKFLOW

## Step 1 — Dev Login

Open:

```
http://localhost:8000/admin_PATCHED.html
```

Click:

```
Dev Login (researcher)
```

This stores a JWT in localStorage.

---

## Step 2 — Experimenter Dashboard

Go to:

```
http://localhost:8000/experimenter_dashboard_improved.html
```

You can now:

- Create experiments
- Import stimuli
- Assign stimuli
- Publish experiments

---

## Step 3 — Subject Interface

```
http://localhost:8000/subject_interface_complete.html?exp=<experiment_id>
```

This runs the adaptive preference engine.

---

## Step 4 — Results Dashboard

```
http://localhost:8000/results_dashboard.html
```

Exports:

- Stimulus pairwise choices
- Session logs
- Experiment summaries

---

# 11. TROUBLESHOOTING

### “Failed to fetch experiments / stimuli”
Cause: you did not dev-login.
Fix: go to admin page → click Dev Login.

### Unauthorized / 401 errors
Cause: JWT missing or expired.
Fix: Dev Login again.

### Frontend pages blank or navigation broken
Cause: you moved HTML files out of `frontend/`.
Fix: put all files back exactly where they were.

### Backend import errors
Cause: project folder structure was changed.
Fix: restore the correct layout.

### Database errors
Cause: schema not loaded.
Fix:
```bash
psql "$DATABASE_URL" -f database/schema.sql
```

---

# 12. HOW NOT TO BREAK THE SYSTEM

### ❌ Do NOT:

- Move files out of `backend/`
- Move HTML out of `frontend/`
- Flatten the repo
- Commit .venv/ or backend/.env
- Rename folders

### ✔ Do:

- Edit inside files, not move them
- Add new files if needed
- Keep navigation paths intact
- Always Dev Login first

---

# 13. GIT & REPO HYGIENE

## Do NOT push these:

```
.venv/
backend/venv/
backend/.env
__pycache__/
```

Add to .gitignore:

```gitignore
.venv/
backend/venv/
backend/.env
__pycache__/
```

## Safe to push:

- Python files
- HTML files
- New docs
- Real code changes

---

# 14. Optional: One-Command Starter Script

Create `dev_run.sh`:

```bash
#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
set -a; source backend/.env; set +a
python backend/api.py
```

Make it executable:

```bash
chmod +x dev_run.sh
```

Run backend with:

```bash
./dev_run.sh
```

---

You are now fully set up to run the entire Adaptive Preference Testing System end-to-end.
