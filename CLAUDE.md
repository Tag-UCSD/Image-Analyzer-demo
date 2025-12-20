# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Workspace Overview

This is a **multi-project workspace** focused on image analysis and data visualization systems. The workspace contains several independent projects, each with their own architecture and purpose.

## Project Structure

```
/Image_Analyzer/
├── graphical-model/          # Bayesian causal modeling for interior psychology
├── image-tagger/             # Image tagging and classification system
├── article-eater/            # Article analysis and processing system
├── knowledge-graph-ui/       # Graph visualization interface
└── experiments/              # Experimental/prototype code
```

## Projects

### 1. graphical-model/

**Bayesian Image-to-Psychology System** - Predicts psychological outcomes (stress, focus, satisfaction) from interior space images using causal inference.

**Tech Stack:** Python, PyMC, FastAPI, PostgreSQL, vanilla JavaScript
**Status:** 45% complete (database + statistical engine done, API + frontend implemented)

**Quick Start:**
```bash
cd graphical-model
pip install -r requirements.txt
cd database && ./setup_database.sh
uvicorn api.main:app --reload
```

**See:** `graphical-model/CLAUDE.md` for detailed architecture and commands

**Key Features:**
- Bayesian causal inference (not black-box ML)
- Do-calculus for interventional queries
- Goldilocks functions for optimal-level relationships
- Full uncertainty quantification with credible intervals
- Provenance tracking to literature sources

### 2. image-tagger/

**Image Tagging System** - System for tagging and classifying images.

**Location:** `image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full/`

**Documentation:** See `.docx` files in `image-tagger/` directory

### 3. article-eater/

**Article Analysis System** - Processes and analyzes academic articles.

**Location:** `article-eater/Article_Eater_v20_7_43_repo/`

**Documentation:** See `.docx` files in `article-eater/` directory

### 4. knowledge-graph-ui/

**Graph Visualization Interface** - UI for exploring knowledge graphs.

**Status:** Minimal README only

### 5. experiments/

**Experimental Code** - Prototypes and experimental features.

## Working with This Workspace

### Navigating Between Projects

Each project is independent with its own dependencies and setup:

```bash
# Always cd into the specific project first
cd graphical-model
# Then run project-specific commands

cd ../image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full
# Different project, different structure
```

### Project-Specific Documentation

- **graphical-model:** Has comprehensive `CLAUDE.md` with detailed architecture, commands, and patterns
- **image-tagger:** Refer to Technical Lead Runbook `.docx` files
- **article-eater:** Refer to Overview and Usage Guide `.docx` files

### Common Patterns Across Projects

1. **Python Virtual Environments:** Most Python projects use venvs - look for `venv/`, `bn_venv/`, or similar
2. **Documentation:** Mix of Markdown (`.md`) and Word documents (`.docx`)
3. **Configuration:** Look for `.env.example`, `config/`, or similar in each project root

## Which Project Should I Work On?

When the user asks you to work on something, determine the context:

- **Bayesian modeling, causal inference, psychology predictions** → `graphical-model/`
- **Image tagging, classification** → `image-tagger/`
- **Article processing, analysis** → `article-eater/`
- **Graph visualization UI** → `knowledge-graph-ui/`

**When in doubt, ask the user which project they're referring to.**

## Important Notes

### graphical-model Specifics

This is the most developed project in the workspace with:
- Complete documentation in `graphical-model/CLAUDE.md`
- Production-ready statistical engine
- FastAPI REST API
- Frontend applications
- Comprehensive test suite

**CRITICAL:** Uses synthetic data only. Not trained on real images or human ratings.

### File Locations

Since this is a multi-project workspace, always use full paths when referencing files:

```bash
# GOOD - explicit path
/Users/taggertsmith/Desktop/Image_Analyzer/graphical-model/api/main.py

# BAD - ambiguous in multi-project workspace
api/main.py
```

## Common Workspace Commands

```bash
# List all projects
ls /Users/taggertsmith/Desktop/Image_Analyzer/

# Navigate to a specific project
cd /Users/taggertsmith/Desktop/Image_Analyzer/graphical-model

# Search across all projects (use with caution - large workspace)
grep -r "search_term" /Users/taggertsmith/Desktop/Image_Analyzer/ --exclude-dir=node_modules --exclude-dir=venv
```

## Getting Started

1. **Ask the user which project** they want to work on
2. **Navigate to that project's directory**
3. **Read that project's specific documentation** (CLAUDE.md, README.md, or .docx files)
4. **Follow that project's setup instructions**

For the most comprehensive and up-to-date information on the graphical-model project specifically, see `graphical-model/CLAUDE.md`.
