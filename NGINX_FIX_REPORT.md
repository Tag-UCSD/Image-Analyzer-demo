# Nginx DNS Resolution Fix - Complete

**Date:** January 19, 2026
**Issue:** Nginx container failing to start due to DNS resolution errors
**Status:** ✅ RESOLVED

---

## Problem Description

### Original Error

```
nginx: [emerg] host not found in upstream "graphical-model:8001"
Container exits immediately on startup
```

### Root Cause

Nginx resolves `upstream` block hostnames **at config-load time** (during startup), before Docker's internal DNS service is available. This is a known timing issue in Docker Compose environments where services start in parallel.

---

## Solution Implemented

### 1. Added Docker DNS Resolver

```nginx
# Enable runtime DNS resolution using Docker's internal DNS
resolver 127.0.0.11 valid=10s ipv6=off;
resolver_timeout 5s;
```

### 2. Removed Static Upstream Blocks

Eliminated all static `upstream` blocks that resolved at config-load time:

```nginx
# REMOVED - these resolved at startup
upstream graphical_model {
  server graphical-model:8001;
}
```

### 3. Added Dynamic Proxy Configuration

Used variables and rewrite rules to force runtime DNS resolution:

```nginx
location /api/graphical/ {
  set $graphical_backend "graphical-model:8001";
  rewrite ^/api/graphical/(.*)$ /api/v1/$1 break;
  proxy_pass http://$graphical_backend;
  # ... headers ...
}
```

**How This Works:**
- `set $graphical_backend` - Variable forces runtime resolution
- `rewrite ... break` - Transforms request path before proxying
- `proxy_pass http://$graphical_backend` - Uses variable (dynamic DNS)

---

## Verification Results

### All Services Healthy ✅

```
SERVICE              PORT    STATUS           HEALTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
postgres            5432    Up 44min         ✅ healthy
redis               6379    Up 44min         ✅ healthy
graphical-model     8001    Up 44min         ✅ healthy
image-tagger        8002    Up 44min         ✅ healthy
article-eater       8003    Up 44min         ✅ healthy
knowledge-graph     8004    Up 44min         ✅ healthy
nginx               8080    Up 2min          ✅ healthy
```

### API Gateway Tests - All Passing ✅

```bash
# Graphical Model
$ curl http://localhost:8080/api/graphical/health
{"status":"healthy","database":"healthy","models":"healthy"}
✅ PASS

# Image Tagger
$ curl http://localhost:8080/api/tagger/health
{"status":"ok","module":"image-tagger","version":"dev"}
✅ PASS

# Article Eater
$ curl http://localhost:8080/api/article/healthz
{"status":"ok","version":"19.0.0","features":{...}}
✅ PASS

# Knowledge Graph
$ curl http://localhost:8080/api/graph/health
{"status":"ok","module":"knowledge-graph-ui","database":"unavailable"}
✅ PASS (database unavailable is expected - not yet integrated)

# Frontend Shell
$ curl http://localhost:8080/
<!doctype html>...
✅ PASS
```

---

## Path Routing Confirmation

### API Proxy Mappings

| Gateway Path | Backend Target | Backend Port |
|-------------|----------------|--------------|
| `/api/graphical/*` → | `graphical-model:8001/api/v1/*` | 8001 |
| `/api/tagger/*` → | `image-tagger:8002/*` | 8002 |
| `/api/article/*` → | `article-eater:8003/*` | 8003 |
| `/api/graph/*` → | `knowledge-graph:8004/*` | 8004 |

### Frontend Static File Mappings

| Gateway Path | Mounted Directory |
|-------------|-------------------|
| `/` | `frontend-shell/dist` |
| `/graphical/` | `graphical-model/frontend-v2/dist` |
| `/article/` | `article-eater/.../frontend` |
| `/graph/` | `knowledge-graph-ui/.../static-frontend` |
| `/tagger/`, `/workbench/`, `/monitor/`, `/admin/`, `/explorer/` | `image-tagger/.../frontend` |

---

## Technical Details

### Why Variables Fix DNS Issues

**Problem with upstream blocks:**
```nginx
upstream backend {
  server hostname:8001;  # Resolved ONCE at config load
}
```

**Solution with variables:**
```nginx
set $backend "hostname:8001";  # Resolved at EACH request
proxy_pass http://$backend;
```

When nginx uses variables in `proxy_pass`, it:
1. Queries DNS resolver (127.0.0.11) at **request time**
2. Caches result for `valid=10s` duration
3. Automatically retries if backend becomes unavailable

### Path Rewriting Logic

```nginx
# Request: /api/graphical/health
rewrite ^/api/graphical/(.*)$ /api/v1/$1 break;
# Result: /api/v1/health

# Request: /api/tagger/health
rewrite ^/api/tagger/(.*)$ /$1 break;
# Result: /health

# Request: /api/article/healthz
rewrite ^/api/article/(.*)$ /$1 break;
# Result: /healthz
```

The `break` flag prevents further rewrite rule processing.

---

## Files Modified

**Primary:**
- `/Users/taggertsmith/Desktop/Image_Analyzer/integration/nginx/nginx.conf`

**Changes:**
1. Added resolver directives (lines 14-15)
2. Removed 4 upstream blocks
3. Updated 4 location blocks with variables and rewrites (lines 86-128)

---

## Impact on Integration

### Pre-Fix Status
- ❌ Nginx container: Failing to start
- ❌ Gateway access: Not available
- ⚠️ Backend access: Direct ports only (8001-8004)
- ⚠️ Frontend shell: Not accessible

### Post-Fix Status
- ✅ Nginx container: Running and healthy
- ✅ Gateway access: Fully functional on port 8080
- ✅ Backend access: Available via gateway AND direct ports
- ✅ Frontend shell: Accessible at http://localhost:8080/

### Integration Readiness
**STATUS: ✅ READY**

The nginx gateway is now fully operational and ready for DATA_FLOW_INTEGRATION_PLAN.md execution. All backend services are accessible through the unified gateway, and path routing is working correctly.

---

## Lessons Learned

1. **Docker DNS Timing:** Always use dynamic DNS resolution in Docker Compose environments
2. **Upstream Blocks:** Avoid static upstreams when service discovery is needed
3. **Variable Proxy Pass:** Forces runtime DNS resolution
4. **Path Rewriting:** Necessary when backend paths differ from gateway paths

---

## Next Steps

With the nginx gateway now operational:
1. ✅ All infrastructure validation complete
2. ✅ Ready to begin Phase 1 of DATA_FLOW_INTEGRATION_PLAN.md
3. ✅ Gateway will support cross-module API calls during integration

---

## Validation Commands

```bash
# Check all services
docker compose -f integration/docker-compose.unified.yml ps

# Test gateway health
curl http://localhost:8080/api/graphical/health
curl http://localhost:8080/api/tagger/health
curl http://localhost:8080/api/article/healthz
curl http://localhost:8080/api/graph/health

# Test frontend
open http://localhost:8080/
```
