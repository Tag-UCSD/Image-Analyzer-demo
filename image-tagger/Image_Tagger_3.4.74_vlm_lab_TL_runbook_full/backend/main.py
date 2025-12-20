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
    Strip a known prefix from incoming paths while preserving original routing.
    """

    def __init__(self, app: Callable, prefix: str) -> None:
        self.app = app
        self.prefix = prefix.rstrip("/")

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope["type"] in {"http", "websocket"}:
            path = scope.get("path", "")
            if path == self.prefix or path.startswith(f"{self.prefix}/"):
                scope = dict(scope)
                scope["path"] = path[len(self.prefix):] or "/"
                scope["root_path"] = f"{scope.get('root_path', '')}{self.prefix}"
        await self.app(scope, receive, send)


app = FastAPI(
    title=f"Image Tagger v3 (v{VERSION})",
    description="Unified API for Tagger Workbench, Supervisor, Admin, and Explorer.",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(PrefixStripMiddleware, prefix="/api/v1/tagger")

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
