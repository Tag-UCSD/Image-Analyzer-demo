# Phase 3 Log

## Planned Changes
- Create unified frontend shell under `integration/frontend-shell` (Vite + React) with shared navigation and module frames.
- Match styling to existing article-eater and image-tagger design patterns (panels/cards/nav), extracting palette/typography/spacing tokens.
- Configure frontend to proxy API calls through the Nginx gateway using `/api/{module}` routes (or `/api/v1/{module}` if needed).
- Add minimal build artifacts for Nginx static serving.

## Notes
- Phase 3 gate check failed initially due to missing frontend shell files; will address during implementation.
- Frontend shell implemented with Vite/React and article-eater inspired design tokens.
- Module embedding uses iframe with per-module UI URL environment variables.
- Build completed with npm; `npm install` reported 2 moderate vulnerabilities (not remediated).
- Phase 3 gate check passed after build.
- Added Nginx routes to serve module UIs at `/graphical/`, `/article/`, `/graph/`, and `/tagger/`.
- Frontend shell now defaults module URLs to those Nginx routes when `VITE_*_UI_URL` is not set.
- Nginx root moved to `/usr/share/nginx/html/shell` to allow mounting module UIs alongside the shell.
- Image-tagger apps built to `frontend/dist/{workbench,monitor,admin,explorer}` and served at `/workbench/`, `/monitor/`, `/admin/`, `/explorer/`.
