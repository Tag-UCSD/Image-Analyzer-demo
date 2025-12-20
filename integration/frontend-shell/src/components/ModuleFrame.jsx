import React, { useState } from 'react';

export default function ModuleFrame({ title, description, url, envKey }) {
  const [loaded, setLoaded] = useState(false);

  if (!url) {
    return (
      <section className="module-frame">
        <div className="panel">
          <div className="panel-header">
            <div>
              <h2>{title}</h2>
              <p>{description}</p>
            </div>
          </div>
          <div className="panel-body">
            <div className="empty-state">
              <div className="empty-icon">Configure</div>
              <div className="empty-text">
                Set the module UI URL in `{envKey}` to embed this tool.
              </div>
            </div>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="module-frame">
      <div className="panel">
        <div className="panel-header">
          <div>
            <h2>{title}</h2>
            <p>{description}</p>
          </div>
          <a className="panel-link" href={url} target="_blank" rel="noreferrer">
            Open in new tab
          </a>
        </div>
        <div className="panel-body">
          <div className={`module-shell ${loaded ? 'is-loaded' : ''}`}>
            {!loaded && <div className="module-loading">Loading module…</div>}
            <iframe
              title={`${title} module`}
              src={url}
              onLoad={() => setLoaded(true)}
              className="module-iframe"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
