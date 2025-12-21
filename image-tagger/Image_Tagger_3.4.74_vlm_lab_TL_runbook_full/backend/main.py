from fastapi import FastAPI
from typing import Callable
from fastapi.staticfiles import StaticFiles

from backend.services.storage import get_image_storage_root
from backend.api import (
    v1_annotation,
    v1_admin,
    v1_supervision,
    v1_discovery,
    v1_bn_export,
    v1_debug,
    v1_features,
    v1_vlm_health,
)
from backend.versioning import VERSION

# v3 Enterprise Application Entry Point
class PrefixStripMiddleware:
    """
    Strip known prefixes from incoming paths while preserving original routing.
    Handles multiple potential prefixes (e.g. /api/v1/tagger, /api/v1/explorer, /api/v1/debug).
    """

    def __init__(self, app: Callable, prefixes: list[str]) -> None:
        self.app = app
        self.prefixes = [p.rstrip("/") for p in prefixes]

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope["type"] in {"http", "websocket"}:
            path = scope.get("path", "")
            for prefix in self.prefixes:
                if path == prefix or path.startswith(f"{prefix}/"):
                    scope = dict(scope)
                    scope["path"] = path[len(prefix):] or "/"
                    scope["root_path"] = f"{scope.get('root_path', '')}{prefix}"
                    break
        await self.app(scope, receive, send)


app = FastAPI(
    title=f"Image Tagger v3 (v{VERSION})",
    description="Unified API for Tagger Workbench, Supervisor, Admin, and Explorer.",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Robustly handle multiple prefixes for local dev vs Nginx proxy
app.add_middleware(
    PrefixStripMiddleware, 
    prefixes=[
        "/api/v1/tagger", # Legacy support if needed
        "/api",           # Main fix: /api/v1/explorer -> /v1/explorer
    ]
)

# Router wiring
app.include_router(v1_annotation.router)
app.include_router(v1_admin.router)
app.include_router(v1_supervision.router)
app.include_router(v1_discovery.router)
app.include_router(v1_bn_export.router)
app.include_router(v1_debug.router)
app.include_router(v1_features.router)
app.include_router(v1_vlm_health.router)

# Static file mount for image assets
IMAGE_STORAGE_ROOT = get_image_storage_root()
app.mount("/static", StaticFiles(directory=str(IMAGE_STORAGE_ROOT)), name="static")

# ============================================================================
# STARTUP / SEEDING
# ============================================================================
from backend.database.core import SessionLocal, engine
from backend.models import Base, Attribute
from backend.scripts import seed_attributes, seed_tool_configs

@app.on_event("startup")
def startup_event():
    """Ensure database is seeded on startup."""
    print("[main] Running startup checks...")
    
@app.on_event("startup")
def startup_event():
    """Ensure database is seeded on startup."""
    print("[main] Running startup checks...")
    
    try:
        # Ensure tables exist
        Base.metadata.create_all(bind=engine)
    
        db = SessionLocal()
        try:
            # Check Attributes
            attr_count = db.query(Attribute).count()
            if attr_count == 0:
                print("[main] Attribute registry empty. seeding...")
                try:
                    seed_attributes.seed()
                except Exception as e:
                    print(f"[main] Failed to seed attributes: {e}")
            else:
                print(f"[main] Attribute registry has {attr_count} entries.")

            # Check Tool Configs
            try:
                 seed_tool_configs.seed()
            except Exception as e:
                print(f"[main] Failed to seed tool configs: {e}")
                
            # Check Images
            from backend.models.assets import Image
            from backend.scripts import import_images_from_json
            import os
            
            image_count = db.query(Image).count()
            if image_count == 0:
                print("[main] Image table empty. seeding sample images...")
                seed_json_path = os.path.join("backend", "data", "seed_images.json")
                try:
                    import_images_from_json.import_images(seed_json_path)
                except Exception as e:
                    print(f"[main] Failed to seed images: {e}")
            else:
                print(f"[main] Image table has {image_count} entries.")
        finally:
            db.close()
            
    except Exception as e:
        print(f"[main] Startup seeding/DB error: {e}")

@app.get("/health")
def health_check() -> dict:
    """Kubernetes/Docker Health Probe."""
    return {"status": "ok", "module": "image-tagger", "version": VERSION}


@app.get("/")
def root():
    return {
        "message": "Image Tagger v3 API",
        "docs": "/docs",
        "workbench_api": "/v1/workbench/next",
    }
