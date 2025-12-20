import React, { useMemo, useState } from 'react';

import ModuleFrame from '../components/ModuleFrame.jsx';

const surfaces = [
  {
    id: 'workbench',
    title: 'Tagger Workbench',
    description: 'High-throughput labeling of images and regions.',
  },
  {
    id: 'monitor',
    title: 'Supervisor Monitor',
    description: 'Track IRR, throughput, and QA disagreements.',
  },
  {
    id: 'explorer',
    title: 'Research Explorer',
    description: 'Search and export tagged corpora.',
  },
  {
    id: 'admin',
    title: 'Admin Cockpit',
    description: 'System controls and budget safeguards.',
  },
];

export default function ImageTagger({ url, gateway }) {
  const [activeSurface, setActiveSurface] = useState('workbench');
  const surfaceUrls = useMemo(() => {
    const root = gateway || window.location.origin;
    const normalized = (url || '').trim();
    let baseRoot = root;

    if (normalized) {
      const match = normalized.match(/^(.*)\/(workbench|monitor|explorer|admin)\/?$/);
      if (match) {
        baseRoot = match[1];
      } else {
        baseRoot = normalized.replace(/\/$/, '');
      }
    }

    return {
      workbench: `${baseRoot}/workbench/`,
      monitor: `${baseRoot}/monitor/`,
      explorer: `${baseRoot}/explorer/`,
      admin: `${baseRoot}/admin/`,
    };
  }, [gateway, url]);

  const active = surfaces.find((surface) => surface.id === activeSurface);
  const activeUrl = surfaceUrls[activeSurface];

  return (
    <section className="module-frame">
      <div className="panel">
        <div className="panel-header">
          <div>
            <h2>Image Tagger Surfaces</h2>
            <p>Select a surface to embed. Each surface opens in a new tab as well.</p>
          </div>
          <a
            className="panel-link"
            href={`${gateway || window.location.origin}/tagger/`}
            target="_blank"
            rel="noreferrer"
          >
            Portal page
          </a>
        </div>
        <div className="panel-body">
          <div className="surface-grid">
            {surfaces.map((surface) => (
              <button
                key={surface.id}
                className={`surface-card ${surface.id === activeSurface ? 'is-active' : ''}`}
                onClick={() => setActiveSurface(surface.id)}
                type="button"
              >
                <div className="surface-title">{surface.title}</div>
                <div className="surface-description">{surface.description}</div>
                <div className="surface-actions">
                  <span className="surface-chip">Embed</span>
                  <a
                    href={surfaceUrls[surface.id]}
                    onClick={(event) => event.stopPropagation()}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Open tab
                  </a>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
      <ModuleFrame
        title={active?.title || 'Image Tagger'}
        description={active?.description || 'Annotate images, inspect attributes, and export training data.'}
        url={activeUrl}
        envKey="VITE_TAGGER_UI_URL"
      />
    </section>
  );
}
