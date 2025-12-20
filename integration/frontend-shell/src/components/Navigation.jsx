import React from 'react';

export default function Navigation({ items, activeId, onSelect, isOpen, onToggle, gateway }) {
  return (
    <aside className={`shell-sidebar ${isOpen ? 'is-open' : ''}`}>
      <div className="sidebar-header">
        <div className="brand-mark">
          <span className="brand-dot" />
          <div>
            <div className="brand-title">Image Analyzer</div>
            <div className="brand-subtitle">Unified Research Console</div>
          </div>
        </div>
        <button className="sidebar-toggle" onClick={onToggle} type="button">
          {isOpen ? 'Close' : 'Menu'}
        </button>
      </div>
      <nav className="nav-list">
        {items.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activeId === item.id ? 'is-active' : ''}`}
            onClick={() => onSelect(item.id)}
            type="button"
          >
            <span className="nav-icon" aria-hidden="true">
              {item.icon}
            </span>
            <span>
              <span className="nav-label">{item.label}</span>
              <span className="nav-meta">{item.meta}</span>
            </span>
          </button>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="status-chip">Gateway: {gateway}</div>
        <div className="status-chip">Phase 3 Shell</div>
      </div>
    </aside>
  );
}
