# Image Analyzer System Integration Plan

## Unified Demo System Architecture

**Document Version:** 1.0
**Created:** December 2024
**Purpose:** Plan for stitching all modules into one integrated demo with clean interfaces, shared databases, and unified navigation.

---

## Executive Summary

This document outlines the plan to integrate four independent projects—**graphical-model**, **image-tagger**, **article-eater**, and **knowledge-graph-ui**—into a single cohesive demo system. The integrated system will feature:

- **Single entry point** with unified navigation
- **Shared PostgreSQL database** with module-specific schemas
- **API Gateway** routing requests to appropriate backends
- **Inter-module data flow** enabling seamless workflows
- **Consistent authentication** across all modules
- **Unified design system** using Adaptive Preference CSS

---

## Current State Analysis

### Module Inventory

| Module | Backend | Database | Port | API Prefix | Frontend |
|--------|---------|----------|------|------------|----------|
| **graphical-model** | FastAPI | PostgreSQL | 8000 | `/api/v1` | Vanilla JS |
| **image-tagger** | FastAPI | PostgreSQL | 8080 | `/v1` | React Micro-frontends |
| **article-eater** | FastAPI | SQLite | 8000 | Mixed | Streamlit/HTML |
| **knowledge-graph-ui** | FastAPI | In-memory | 8000 | `/api/v1` | Vanilla JS/Cytoscape |

### Data Flow Between Modules

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INTEGRATED WORKFLOW                                │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
  │  ARTICLE EATER   │ ──────▶ │  KNOWLEDGE       │ ──────▶ │  GRAPHICAL       │
  │                  │         │  GRAPH UI        │         │  MODEL           │
  │  - Extract       │         │                  │         │                  │
  │    findings      │         │  - Visualize     │         │  - Bayesian      │
  │  - Generate      │         │    causal graph  │         │    inference     │
  │    design rules  │         │  - Evidence      │         │  - Do-calculus   │
  │  - Literature    │         │    provenance    │         │  - Predictions   │
  │    evidence      │         │                  │         │                  │
  └──────────────────┘         └──────────────────┘         └──────────────────┘
           │                            │                            │
           │                            │                            │
           ▼                            ▼                            ▼
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                           IMAGE TAGGER                                    │
  │                                                                          │
  │  - Tag images with visual attributes                                     │
  │  - Train models on human ratings                                         │
  │  - Validate causal relationships experimentally                          │
  │  - Export data for Bayesian network training                             │
  └──────────────────────────────────────────────────────────────────────────┘
```

### Integration Points

1. **Article Eater → Knowledge Graph**: Extracted findings and rules populate evidence for causal edges
2. **Knowledge Graph → Graphical Model**: Causal graph structure feeds Bayesian model specification
3. **Image Tagger → Graphical Model**: Tagged images provide training data for predictions
4. **Graphical Model → Knowledge Graph**: Updated posteriors refine edge effect sizes
5. **All Modules → Shared Database**: Common evidence base and provenance tracking

---

## Target Architecture

### System Diagram

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                              UNIFIED FRONTEND                                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     Navigation Shell (ap-shell-gradient)                 │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐  │   │
│  │  │  Home  │ │ Tagger │ │Evidence│ │  Graph │ │Analyzer│ │   Admin    │  │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                         Module Content Area                              │   │
│  │                                                                          │   │
│  │   (Renders selected module's UI with consistent styling)                 │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                              NGINX API GATEWAY                                  │
│                                                                                 │
│    /api/graphical/*  →  graphical-model:8001                                   │
│    /api/tagger/*     →  image-tagger:8002                                      │
│    /api/evidence/*   →  article-eater:8003                                     │
│    /api/graph/*      →  knowledge-graph:8004                                   │
│    /api/auth/*       →  auth-service:8005                                      │
│    /static/*         →  nginx static files                                     │
│                                                                                 │
└────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND SERVICES                                   │
│                                                                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐          │
│  │  Graphical   │ │   Image      │ │   Article    │ │  Knowledge   │          │
│  │    Model     │ │   Tagger     │ │    Eater     │ │    Graph     │          │
│  │   :8001      │ │   :8002      │ │   :8003      │ │   :8004      │          │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬───────┘          │
│         │                │                │                │                   │
│         └────────────────┴────────────────┴────────────────┘                   │
│                                   │                                             │
│                                   ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                         SHARED POSTGRESQL DATABASE                        │  │
│  │                                                                           │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │  │
│  │  │  core       │ │  tagger     │ │  evidence   │ │  graphical  │         │  │
│  │  │  schema     │ │  schema     │ │  schema     │ │  schema     │         │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘         │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Infrastructure Foundation

### 1.1 Docker Compose Orchestration

Create a unified `docker-compose.unified.yml` at the workspace root:

```yaml
version: '3.8'

services:
  # ============================================
  # SHARED INFRASTRUCTURE
  # ============================================

  postgres:
    image: postgres:15
    container_name: image-analyzer-db
    environment:
      POSTGRES_DB: image_analyzer
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD:-devpassword}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: image-analyzer-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # ============================================
  # API GATEWAY
  # ============================================

  nginx:
    image: nginx:alpine
    container_name: image-analyzer-gateway
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./frontend-unified/dist:/usr/share/nginx/html:ro
    depends_on:
      - graphical-model
      - image-tagger
      - article-eater
      - knowledge-graph

  # ============================================
  # BACKEND SERVICES
  # ============================================

  graphical-model:
    build:
      context: ./graphical-model
      dockerfile: Dockerfile
    container_name: graphical-model-api
    environment:
      DATABASE_HOST: postgres
      DATABASE_PORT: 5432
      DATABASE_NAME: image_analyzer
      DATABASE_USER: postgres
      DATABASE_PASSWORD: ${DB_PASSWORD:-devpassword}
      API_PREFIX: /api/v1
    depends_on:
      postgres:
        condition: service_healthy
    expose:
      - "8001"

  image-tagger:
    build:
      context: ./image-tagger/Image_Tagger_3.4.74_vlm_lab_TL_runbook_full
      dockerfile: deploy/Dockerfile
    container_name: image-tagger-api
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD:-devpassword}@postgres:5432/image_analyzer
      SCHEMA_NAME: tagger
    depends_on:
      postgres:
        condition: service_healthy
    expose:
      - "8002"
    volumes:
      - image_storage:/app/storage

  article-eater:
    build:
      context: ./article-eater/Article_Eater_v20_7_43_repo
      dockerfile: Dockerfile
    container_name: article-eater-api
    environment:
      DB_URL: postgresql://postgres:${DB_PASSWORD:-devpassword}@postgres:5432/image_analyzer
      SCHEMA_NAME: evidence
    depends_on:
      postgres:
        condition: service_healthy
    expose:
      - "8003"

  knowledge-graph:
    build:
      context: ./knowledge-graph-ui/GraphExplorer_Static_v3/backend
      dockerfile: Dockerfile
    container_name: knowledge-graph-api
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD:-devpassword}@postgres:5432/image_analyzer
      SCHEMA_NAME: graph
    depends_on:
      postgres:
        condition: service_healthy
    expose:
      - "8004"

volumes:
  postgres_data:
  redis_data:
  image_storage:
```

### 1.2 Database Schema Consolidation

Create unified database initialization scripts in `database/init/`:

**File: `00_extensions.sql`**
```sql
-- Enable required PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search
CREATE EXTENSION IF NOT EXISTS "btree_gist";  -- For exclusion constraints
```

**File: `01_schemas.sql`**
```sql
-- Create schemas for each module
CREATE SCHEMA IF NOT EXISTS core;      -- Shared entities (users, images, etc.)
CREATE SCHEMA IF NOT EXISTS tagger;    -- Image Tagger specific tables
CREATE SCHEMA IF NOT EXISTS evidence;  -- Article Eater tables
CREATE SCHEMA IF NOT EXISTS graphical; -- Graphical Model tables
CREATE SCHEMA IF NOT EXISTS graph;     -- Knowledge Graph tables

-- Set search path to include all schemas
ALTER DATABASE image_analyzer SET search_path TO core, tagger, evidence, graphical, graph, public;
```

**File: `02_core_tables.sql`**
```sql
-- CORE SCHEMA: Shared entities across all modules

-- Users table (shared authentication)
CREATE TABLE core.users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Images table (shared across tagger and graphical-model)
CREATE TABLE core.images (
    image_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    space_type VARCHAR(100),
    source VARCHAR(255),
    uploaded_by UUID REFERENCES core.users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Literature sources (shared between evidence and graphical)
CREATE TABLE core.literature_sources (
    source_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doi VARCHAR(255) UNIQUE,
    title TEXT NOT NULL,
    authors JSONB,
    year INTEGER,
    venue VARCHAR(255),
    abstract TEXT,
    citation_count INTEGER DEFAULT 0,
    full_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_images_space_type ON core.images(space_type);
CREATE INDEX idx_literature_doi ON core.literature_sources(doi);
CREATE INDEX idx_literature_year ON core.literature_sources(year);
```

**File: `03_tagger_schema.sql`**
```sql
-- Import from image-tagger database schema
-- Adapted for PostgreSQL schemas

CREATE TABLE tagger.attributes (
    attribute_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID REFERENCES core.images(image_id),
    attribute_name VARCHAR(100) NOT NULL,
    value FLOAT,
    confidence FLOAT,
    source VARCHAR(50),  -- 'human', 'vlm', 'computed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tagger.tags (
    tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID REFERENCES core.images(image_id),
    tag_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    value VARCHAR(255),
    rater_id UUID REFERENCES core.users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- More tables from image-tagger schema...
```

**File: `04_evidence_schema.sql`**
```sql
-- Migrate from article-eater SQLite to PostgreSQL

CREATE TABLE evidence.articles (
    article_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES core.literature_sources(source_id),
    processing_status VARCHAR(50) DEFAULT 'pending',
    l0_completed_at TIMESTAMP,
    l2_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evidence.findings (
    finding_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    article_id UUID REFERENCES evidence.articles(article_id),
    finding_text TEXT NOT NULL,
    effect_direction VARCHAR(50),
    effect_size FLOAT,
    p_value FLOAT,
    confidence_interval JSONB,
    population TEXT,
    design VARCHAR(100),
    quality VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evidence.rules (
    rule_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_text TEXT NOT NULL,
    confidence FLOAT,
    triangulation_score FLOAT,
    contradiction_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE evidence.rule_evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id UUID REFERENCES evidence.rules(rule_id),
    finding_id UUID REFERENCES evidence.findings(finding_id),
    stance VARCHAR(50),  -- 'supports', 'contradicts', 'qualifies'
    weight FLOAT DEFAULT 1.0
);
```

**File: `05_graphical_schema.sql`**
```sql
-- From graphical-model database schema

CREATE TABLE graphical.model_parameters (
    param_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_version VARCHAR(20) NOT NULL,
    parameter_name VARCHAR(100) NOT NULL,
    posterior_mean FLOAT,
    posterior_sd FLOAT,
    ci_lower FLOAT,
    ci_upper FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE graphical.predictions (
    prediction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID REFERENCES core.images(image_id),
    model_version VARCHAR(20),
    outcome_name VARCHAR(100),
    predicted_mean FLOAT,
    predicted_sd FLOAT,
    ci_lower FLOAT,
    ci_upper FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE graphical.mediator_ratings (
    rating_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID REFERENCES core.images(image_id),
    mediator_name VARCHAR(100) NOT NULL,
    rating_value FLOAT,
    rater_id UUID REFERENCES core.users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**File: `06_graph_schema.sql`**
```sql
-- Shared causal graph structure

CREATE TABLE graph.nodes (
    node_id VARCHAR(100) PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    level VARCHAR(50) NOT NULL,  -- 'attribute', 'mediator', 'outcome'
    node_group VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE graph.edges (
    edge_id VARCHAR(255) PRIMARY KEY,
    from_node VARCHAR(100) REFERENCES graph.nodes(node_id),
    to_node VARCHAR(100) REFERENCES graph.nodes(node_id),
    status VARCHAR(50) DEFAULT 'hypothesized',  -- 'hypothesized', 'supported', 'experimentally_validated'
    effect_mean FLOAT,
    effect_sd FLOAT,
    ci_lower FLOAT,
    ci_upper FLOAT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE graph.edge_evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    edge_id VARCHAR(255) REFERENCES graph.edges(edge_id),
    finding_id UUID REFERENCES evidence.findings(finding_id),
    source_id UUID REFERENCES core.literature_sources(source_id),
    effect_direction VARCHAR(50),
    quality VARCHAR(50),
    notes TEXT
);
```

### 1.3 Nginx Gateway Configuration

**File: `nginx/nginx.conf`**
```nginx
worker_processes auto;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    gzip on;
    gzip_types text/plain application/json application/javascript text/css;

    # Upstream definitions
    upstream graphical_api {
        server graphical-model:8001;
    }

    upstream tagger_api {
        server image-tagger:8002;
    }

    upstream evidence_api {
        server article-eater:8003;
    }

    upstream graph_api {
        server knowledge-graph:8004;
    }

    server {
        listen 80;
        server_name localhost;

        # Static frontend
        root /usr/share/nginx/html;
        index index.html;

        # SPA routing - serve index.html for all frontend routes
        location / {
            try_files $uri $uri/ /index.html;
        }

        # API Gateway routing

        # Graphical Model API
        location /api/graphical/ {
            rewrite ^/api/graphical/(.*)$ /api/v1/$1 break;
            proxy_pass http://graphical_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        # Image Tagger API
        location /api/tagger/ {
            rewrite ^/api/tagger/(.*)$ /v1/$1 break;
            proxy_pass http://tagger_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Article Eater API
        location /api/evidence/ {
            rewrite ^/api/evidence/(.*)$ /$1 break;
            proxy_pass http://evidence_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # Knowledge Graph API
        location /api/graph/ {
            rewrite ^/api/graph/(.*)$ /api/v1/$1 break;
            proxy_pass http://graph_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        # WebSocket support for article-eater
        location /ws {
            proxy_pass http://evidence_api;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }

        # Health check endpoint
        location /health {
            return 200 '{"status": "healthy", "gateway": "nginx"}';
            add_header Content-Type application/json;
        }
    }
}
```

---

## Phase 2: Unified Frontend

### 2.1 Frontend Shell Architecture

Create a new unified frontend that wraps all module UIs:

**File: `frontend-unified/src/App.jsx`** (or vanilla JS equivalent)
```jsx
// Navigation shell with module switching

const MODULES = [
  { id: 'home', name: 'Home', icon: 'home', path: '/' },
  { id: 'tagger', name: 'Image Tagger', icon: 'image', path: '/tagger' },
  { id: 'evidence', name: 'Evidence Extractor', icon: 'document', path: '/evidence' },
  { id: 'graph', name: 'Causal Graph', icon: 'graph', path: '/graph' },
  { id: 'analyzer', name: 'Image Analyzer', icon: 'analytics', path: '/analyzer' },
  { id: 'admin', name: 'Admin', icon: 'settings', path: '/admin' },
];

function App() {
  const [activeModule, setActiveModule] = useState('home');

  return (
    <div className="ap-shell-gradient">
      <NavigationHeader modules={MODULES} active={activeModule} />
      <main className="ap-main-content">
        <ModuleRouter activeModule={activeModule} />
      </main>
      <StatusBar />
    </div>
  );
}
```

### 2.2 Module Integration Approaches

**Option A: Iframe Integration (Simple, Works Now)**
```html
<!-- Each module rendered in iframe with consistent frame -->
<div class="module-frame">
  <iframe
    id="module-content"
    src="/modules/tagger/index.html"
    style="width: 100%; height: calc(100vh - 60px); border: none;">
  </iframe>
</div>
```

**Option B: Micro-Frontend Integration (Recommended for Production)**
- Use Module Federation or single-spa
- Each module exposes its React/JS components
- Shell dynamically loads and mounts modules

**Option C: Full Rebuild (Most Work, Cleanest Result)**
- Rebuild all module UIs in consistent framework
- Share component library
- Unified state management

### 2.3 Unified Navigation Component

**File: `frontend-unified/src/components/Navigation.js`**
```javascript
class UnifiedNavigation {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.modules = [
      { id: 'home', name: 'Home', path: '/', icon: '🏠' },
      { id: 'tagger', name: 'Image Tagger', path: '/tagger', icon: '🏷️',
        description: 'Tag and annotate architectural images' },
      { id: 'evidence', name: 'Evidence Extractor', path: '/evidence', icon: '📚',
        description: 'Extract findings from academic papers' },
      { id: 'graph', name: 'Causal Graph', path: '/graph', icon: '🔗',
        description: 'Explore causal relationships' },
      { id: 'analyzer', name: 'Image Analyzer', path: '/analyzer', icon: '🔬',
        description: 'Predict psychological outcomes' },
      { id: 'admin', name: 'Admin', path: '/admin', icon: '⚙️',
        description: 'System administration' },
    ];
    this.render();
  }

  render() {
    this.container.innerHTML = `
      <nav class="ap-nav unified-nav">
        <div class="nav-brand">
          <span class="brand-icon">🧠</span>
          <span class="brand-text">Image Analyzer</span>
        </div>
        <ul class="nav-modules">
          ${this.modules.map(m => `
            <li class="nav-item ${window.location.pathname.startsWith(m.path) ? 'active' : ''}">
              <a href="${m.path}" class="nav-link" title="${m.description || m.name}">
                <span class="nav-icon">${m.icon}</span>
                <span class="nav-text">${m.name}</span>
              </a>
            </li>
          `).join('')}
        </ul>
        <div class="nav-user">
          <span id="user-info">Guest</span>
          <button id="login-btn" class="ap-btn-sm">Login</button>
        </div>
      </nav>
    `;
  }
}
```

### 2.4 Shared API Client

**File: `frontend-unified/src/api/client.js`**
```javascript
/**
 * Unified API client for all modules
 */
class UnifiedAPIClient {
  constructor(baseUrl = '') {
    this.baseUrl = baseUrl;
    this.token = localStorage.getItem('auth_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token && { 'Authorization': `Bearer ${this.token}` }),
      ...options.headers,
    };

    const response = await fetch(url, { ...options, headers });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // ===== Graphical Model API =====
  graphical = {
    predict: (attributes) =>
      this.request('/api/graphical/predict', { method: 'POST', body: JSON.stringify(attributes) }),
    intervene: (data) =>
      this.request('/api/graphical/intervene', { method: 'POST', body: JSON.stringify(data) }),
    getImages: (page = 1, size = 20) =>
      this.request(`/api/graphical/images?page=${page}&page_size=${size}`),
    getCausalGraph: (version = '1.0') =>
      this.request(`/api/graphical/causal-graph/${version}`),
    health: () =>
      this.request('/api/graphical/health'),
  };

  // ===== Image Tagger API =====
  tagger = {
    nextImage: () =>
      this.request('/api/tagger/workbench/next'),
    submitTags: (imageId, tags) =>
      this.request('/api/tagger/annotation/submit', {
        method: 'POST',
        body: JSON.stringify({ image_id: imageId, tags })
      }),
    getAttributes: (imageId) =>
      this.request(`/api/tagger/discovery/attributes/${imageId}`),
    exportBN: (format = 'json') =>
      this.request(`/api/tagger/bn-export?format=${format}`),
    health: () =>
      this.request('/api/tagger/health'),
  };

  // ===== Article Eater API =====
  evidence = {
    submitJob: (jobType, params) =>
      this.request('/api/evidence/jobs/', {
        method: 'POST',
        body: JSON.stringify({ job_type: jobType, params })
      }),
    getJob: (jobId) =>
      this.request(`/api/evidence/jobs/${jobId}`),
    getArticles: (limit = 50) =>
      this.request(`/api/evidence/library/?limit=${limit}`),
    getFindings: (articleId) =>
      this.request(`/api/evidence/findings?article_id=${articleId}`),
    getRules: (limit = 50) =>
      this.request(`/api/evidence/rules?limit=${limit}`),
    health: () =>
      this.request('/api/evidence/healthz'),
  };

  // ===== Knowledge Graph API =====
  graph = {
    getGraph: (version = 'v1_demo') =>
      this.request(`/api/graph/graph/${version}`),
    getEdge: (edgeId) =>
      this.request(`/api/graph/edges/${edgeId}`),
    predict: (attributes) =>
      this.request('/api/graph/predict', { method: 'POST', body: JSON.stringify(attributes) }),
  };

  // ===== Cross-Module Operations =====

  /**
   * Full workflow: Extract findings → Update graph → Retrain model
   */
  async processNewEvidence(paperDoi) {
    // 1. Submit to article-eater
    const job = await this.evidence.submitJob('L2_extract', { doi: paperDoi });

    // 2. Poll for completion
    let status = 'pending';
    while (status === 'pending' || status === 'running') {
      await new Promise(resolve => setTimeout(resolve, 2000));
      const jobStatus = await this.evidence.getJob(job.job_id);
      status = jobStatus.status;
    }

    // 3. Get extracted findings
    const findings = await this.evidence.getFindings(job.article_id);

    // 4. Update causal graph (would need backend endpoint)
    // await this.graph.updateFromFindings(findings);

    return { job, findings };
  }

  /**
   * Predict from image: Get attributes → Run inference → Display results
   */
  async predictFromImage(imageId) {
    // 1. Get image attributes from tagger
    const attributes = await this.tagger.getAttributes(imageId);

    // 2. Run Bayesian prediction
    const prediction = await this.graphical.predict(attributes);

    // 3. Get causal explanation from graph
    const graph = await this.graph.getGraph();

    return { attributes, prediction, graph };
  }
}

// Export singleton
const api = new UnifiedAPIClient();
export default api;
```

---

## Phase 3: Inter-Module Communication

### 3.1 Event Bus for Real-Time Updates

**File: `frontend-unified/src/events/eventBus.js`**
```javascript
/**
 * Cross-module event bus for real-time coordination
 */
class EventBus {
  constructor() {
    this.listeners = new Map();
    this.websocket = null;
  }

  // Subscribe to events
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event).add(callback);
    return () => this.off(event, callback);
  }

  // Unsubscribe
  off(event, callback) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).delete(callback);
    }
  }

  // Emit event to all listeners
  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => callback(data));
    }
  }

  // Connect to WebSocket for real-time updates
  connectWebSocket(url = '/ws') {
    this.websocket = new WebSocket(`ws://${window.location.host}${url}`);

    this.websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.emit(data.type, data.payload);
    };

    this.websocket.onclose = () => {
      // Reconnect after delay
      setTimeout(() => this.connectWebSocket(url), 5000);
    };
  }
}

// Event types
export const EVENTS = {
  // Evidence module events
  FINDING_EXTRACTED: 'finding:extracted',
  RULE_GENERATED: 'rule:generated',
  JOB_COMPLETED: 'job:completed',

  // Tagger module events
  IMAGE_TAGGED: 'image:tagged',
  ATTRIBUTE_UPDATED: 'attribute:updated',

  // Graph module events
  EDGE_UPDATED: 'edge:updated',
  NODE_ADDED: 'node:added',

  // Graphical model events
  MODEL_RETRAINED: 'model:retrained',
  PREDICTION_COMPLETED: 'prediction:completed',

  // System events
  USER_LOGGED_IN: 'user:login',
  USER_LOGGED_OUT: 'user:logout',
  ERROR: 'error',
};

export const eventBus = new EventBus();
```

### 3.2 Backend Message Queue (Redis Pub/Sub)

**File: `shared/messaging.py`** (shared across backends)
```python
"""
Cross-module messaging using Redis Pub/Sub
"""
import redis
import json
from typing import Callable, Any

class MessageBus:
    def __init__(self, redis_url: str = "redis://redis:6379"):
        self.redis = redis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()
        self._handlers = {}

    def publish(self, channel: str, message: dict):
        """Publish message to channel"""
        self.redis.publish(channel, json.dumps(message))

    def subscribe(self, channel: str, handler: Callable[[dict], Any]):
        """Subscribe to channel with handler"""
        self._handlers[channel] = handler
        self.pubsub.subscribe(**{channel: self._message_handler})

    def _message_handler(self, message):
        if message['type'] == 'message':
            channel = message['channel'].decode()
            data = json.loads(message['data'])
            if channel in self._handlers:
                self._handlers[channel](data)

    def run(self):
        """Start listening for messages"""
        for message in self.pubsub.listen():
            pass  # Handled by _message_handler


# Channel definitions
CHANNELS = {
    'EVIDENCE_EXTRACTED': 'evidence:extracted',
    'GRAPH_UPDATED': 'graph:updated',
    'MODEL_RETRAINED': 'model:retrained',
    'IMAGE_PROCESSED': 'image:processed',
}


# Usage in article-eater when finding is extracted:
# message_bus.publish(CHANNELS['EVIDENCE_EXTRACTED'], {
#     'finding_id': finding.id,
#     'article_id': article.id,
#     'edge_candidates': [...],
# })

# Usage in knowledge-graph-ui to listen:
# @message_bus.subscribe(CHANNELS['EVIDENCE_EXTRACTED'])
# def handle_new_evidence(data):
#     update_graph_edges(data['edge_candidates'])
```

### 3.3 Cross-Module API Endpoints

Add new endpoints to each service for inter-module communication:

**Graphical Model - New endpoints:**
```python
# api/routes/integration.py

@router.post("/integration/update-from-evidence")
async def update_from_evidence(evidence: EvidenceUpdate):
    """
    Receive new evidence from article-eater and update priors
    """
    # Update causal graph edge priors
    await update_edge_priors(evidence.edge_id, evidence.findings)

    # Trigger model retraining if needed
    if should_retrain(evidence):
        background_tasks.add_task(retrain_models)

    return {"status": "updated", "edge_id": evidence.edge_id}

@router.get("/integration/export-predictions/{image_id}")
async def export_predictions_for_tagger(image_id: str):
    """
    Export predictions in format suitable for image-tagger
    """
    predictions = await get_predictions(image_id)
    return format_for_tagger(predictions)
```

**Knowledge Graph - New endpoints:**
```python
# Add to main.py

@app.post("/api/v1/edges/update-from-findings")
def update_edges_from_findings(findings: List[FindingInput]):
    """
    Update edge effect sizes based on new extracted findings
    """
    for finding in findings:
        edge_id = finding.edge_id
        if edge_id in EDGES:
            # Update posterior with new evidence
            EDGES[edge_id] = update_edge_posterior(
                EDGES[edge_id],
                finding.effect_size,
                finding.weight
            )

    # Notify other services
    publish_event('graph:updated', {'updated_edges': [f.edge_id for f in findings]})

    return {"status": "updated", "edges_updated": len(findings)}

@app.get("/api/v1/graph/export-for-bayesian")
def export_for_bayesian_model():
    """
    Export graph structure in format for graphical-model training
    """
    return {
        "nodes": [node.dict() for node in NODES],
        "edges": [
            {
                "from": edge.from_node,
                "to": edge.to_node,
                "prior_mean": edge.param.mean,
                "prior_sd": edge.param.sd,
                "status": edge.status,
            }
            for edge in EDGES.values()
        ]
    }
```

---

## Phase 4: Authentication & Authorization

### 4.1 Shared Auth Service

Create a shared authentication module:

**File: `shared/auth/service.py`**
```python
"""
Shared authentication service for all modules
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenData(BaseModel):
    user_id: str
    email: str
    role: str
    exp: datetime


class User(BaseModel):
    user_id: str
    email: str
    name: Optional[str]
    role: str = "user"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user.user_id,
        "email": user.email,
        "role": user.role,
        "exp": expire,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(
            user_id=payload["sub"],
            email=payload["email"],
            role=payload["role"],
            exp=datetime.fromtimestamp(payload["exp"]),
        )
    except JWTError:
        return None


# FastAPI dependency for protected routes
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    token_data = decode_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    if token_data.exp < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    return token_data


async def require_role(required_role: str):
    async def role_checker(user: TokenData = Depends(get_current_user)):
        if user.role != required_role and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{required_role}' required",
            )
        return user
    return role_checker
```

### 4.2 Role-Based Access Control

| Module | Role Required | Notes |
|--------|---------------|-------|
| Home | None | Public landing page |
| Image Tagger - Workbench | `student`, `researcher` | Tag images |
| Image Tagger - Monitor | `supervisor`, `admin` | Review tags |
| Image Tagger - Admin | `admin` | System config |
| Evidence Extractor | `student`, `researcher` | Extract findings |
| Causal Graph | `researcher`, `admin` | View/edit graph |
| Image Analyzer | `student`, `researcher` | Run predictions |
| Admin Dashboard | `admin` | Full system access |

---

## Phase 5: Implementation Roadmap

### Step-by-Step Implementation

#### Step 1: Infrastructure (Est. 2-3 days)
- [ ] Create unified `docker-compose.unified.yml`
- [ ] Write database initialization scripts
- [ ] Configure Nginx gateway
- [ ] Set up Redis for messaging
- [ ] Create shared volume configurations
- [ ] Test individual services start correctly

#### Step 2: Database Migration (Est. 3-4 days)
- [ ] Migrate image-tagger schema to PostgreSQL
- [ ] Migrate article-eater from SQLite to PostgreSQL
- [ ] Create shared tables (core schema)
- [ ] Write data migration scripts for existing data
- [ ] Create foreign key relationships between modules
- [ ] Test all modules connect to shared database

#### Step 3: API Modifications (Est. 4-5 days)
- [ ] Update graphical-model to use new port (8001) and database schema
- [ ] Update image-tagger for PostgreSQL and schema prefix
- [ ] Update article-eater for PostgreSQL
- [ ] Update knowledge-graph for database backend
- [ ] Add integration endpoints to each service
- [ ] Implement shared authentication dependency
- [ ] Test all APIs through gateway

#### Step 4: Frontend Unification (Est. 5-7 days)
- [ ] Create unified navigation shell
- [ ] Implement module router
- [ ] Build shared API client
- [ ] Integrate image-tagger UIs (or iframe initially)
- [ ] Integrate article-eater UI
- [ ] Integrate knowledge-graph UI
- [ ] Integrate graphical-model frontend
- [ ] Apply consistent Adaptive Preference styling
- [ ] Test navigation between modules

#### Step 5: Inter-Module Communication (Est. 3-4 days)
- [ ] Implement Redis pub/sub messaging
- [ ] Create event bus for frontend
- [ ] Wire up cross-module API calls
- [ ] Test evidence → graph → model workflow
- [ ] Test tagger → graphical-model prediction workflow

#### Step 6: Testing & Polish (Est. 3-4 days)
- [ ] End-to-end integration testing
- [ ] Performance testing
- [ ] Security review
- [ ] Documentation updates
- [ ] Demo walkthrough script

**Total Estimated Effort: 20-27 days**

---

## Directory Structure After Integration

```
/Image_Analyzer/
├── CLAUDE.md                          # Root guidance
├── INTEGRATION_PLAN.md                # This document
├── docker-compose.unified.yml         # Unified orchestration
├── .env                               # Environment variables
│
├── database/                          # Shared database config
│   ├── init/
│   │   ├── 00_extensions.sql
│   │   ├── 01_schemas.sql
│   │   ├── 02_core_tables.sql
│   │   ├── 03_tagger_schema.sql
│   │   ├── 04_evidence_schema.sql
│   │   ├── 05_graphical_schema.sql
│   │   └── 06_graph_schema.sql
│   └── migrations/
│
├── nginx/                             # API Gateway
│   ├── nginx.conf
│   └── conf.d/
│       └── upstream.conf
│
├── shared/                            # Shared Python modules
│   ├── auth/
│   │   ├── __init__.py
│   │   └── service.py
│   ├── messaging/
│   │   ├── __init__.py
│   │   └── redis_bus.py
│   └── models/
│       └── common.py
│
├── frontend-unified/                  # Unified frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── Navigation.js
│   │   │   ├── ModuleRouter.js
│   │   │   └── StatusBar.js
│   │   ├── api/
│   │   │   └── client.js
│   │   ├── events/
│   │   │   └── eventBus.js
│   │   └── modules/
│   │       ├── home/
│   │       ├── tagger/
│   │       ├── evidence/
│   │       ├── graph/
│   │       ├── analyzer/
│   │       └── admin/
│   ├── package.json
│   └── vite.config.js
│
├── graphical-model/                   # Bayesian modeling module
│   ├── CLAUDE.md
│   ├── Dockerfile
│   ├── api/
│   └── statistical_engine/
│
├── image-tagger/                      # Image tagging module
│   └── Image_Tagger_3.4.74_.../
│       ├── CLAUDE.md
│       ├── Dockerfile
│       ├── backend/
│       └── frontend/
│
├── article-eater/                     # Evidence extraction module
│   └── Article_Eater_v20_7_43_repo/
│       ├── CLAUDE.md
│       ├── Dockerfile
│       ├── app/
│       └── src/
│
├── knowledge-graph-ui/                # Graph visualization module
│   ├── CLAUDE.md
│   └── GraphExplorer_Static_v3/
│       ├── Dockerfile
│       ├── backend/
│       └── static-frontend/
│
└── experiments/                       # Experimental code
    └── CLAUDE.md
```

---

## Success Criteria

### Functional Requirements
- [ ] User can access all modules from single URL
- [ ] Navigation between modules is seamless (no page reload)
- [ ] User authentication persists across modules
- [ ] Data flows correctly between modules:
  - [ ] Evidence extracted → Graph updated
  - [ ] Graph structure → Bayesian model
  - [ ] Images tagged → Predictions available
- [ ] All existing functionality works in integrated environment

### Non-Functional Requirements
- [ ] Page load time < 3 seconds
- [ ] API response time < 500ms for common operations
- [ ] System handles 10 concurrent users
- [ ] Graceful degradation if one module fails
- [ ] Consistent styling across all modules

### Demo Workflow
1. User logs in via unified login
2. Navigates to Evidence Extractor
3. Submits a paper DOI for processing
4. Views extracted findings
5. Navigates to Causal Graph
6. Sees updated graph with new evidence
7. Navigates to Image Tagger
8. Tags an image with attributes
9. Navigates to Image Analyzer
10. Runs prediction on tagged image
11. Views psychological outcome predictions with causal explanation

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Database migration data loss | High | Full backup before migration, test on staging first |
| API incompatibilities | Medium | Versioned APIs, comprehensive integration tests |
| Performance degradation | Medium | Load testing, caching strategy, database indexing |
| Authentication complexity | Medium | Start with simple JWT, iterate on RBAC |
| Frontend integration issues | Medium | Start with iframes, migrate to micro-frontends |
| Module coupling | Low | Event-driven architecture, clear interface contracts |

---

## Appendix: Quick Reference

### Environment Variables

```bash
# Database
DB_PASSWORD=your_secure_password
DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@postgres:5432/image_analyzer

# Authentication
JWT_SECRET_KEY=your_secure_jwt_secret

# Redis
REDIS_URL=redis://redis:6379

# API URLs (internal)
GRAPHICAL_API_URL=http://graphical-model:8001
TAGGER_API_URL=http://image-tagger:8002
EVIDENCE_API_URL=http://article-eater:8003
GRAPH_API_URL=http://knowledge-graph:8004
```

### Common Commands

```bash
# Start everything
docker-compose -f docker-compose.unified.yml up -d

# View logs
docker-compose -f docker-compose.unified.yml logs -f

# Rebuild specific service
docker-compose -f docker-compose.unified.yml build graphical-model
docker-compose -f docker-compose.unified.yml up -d graphical-model

# Database access
docker-compose exec postgres psql -U postgres -d image_analyzer

# Run migrations
docker-compose exec graphical-model python manage.py migrate

# Health check all services
curl http://localhost/health
curl http://localhost/api/graphical/health
curl http://localhost/api/tagger/health
curl http://localhost/api/evidence/healthz
curl http://localhost/api/graph/health
```

---

**Document Status:** Draft v1.0
**Next Steps:** Review with stakeholders, prioritize implementation phases, begin Phase 1 infrastructure work.
