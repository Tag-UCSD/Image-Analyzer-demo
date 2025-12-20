import React, { useMemo, useState } from 'react';

import Navigation from './components/Navigation.jsx';
import GraphicalModel from './modules/GraphicalModel.jsx';
import ImageTagger from './modules/ImageTagger.jsx';
import ArticleEater from './modules/ArticleEater.jsx';
import KnowledgeGraph from './modules/KnowledgeGraph.jsx';

const moduleConfigs = [
  {
    id: 'graphical',
    label: 'Causal Model',
    meta: 'Graphical Model',
    icon: 'GM',
    title: 'Graphical Model',
    description: 'Bayesian inference, interventions, and prediction outputs.',
    envKey: 'VITE_GRAPHICAL_UI_URL',
    component: GraphicalModel,
  },
  {
    id: 'tagger',
    label: 'Image Tagger',
    meta: 'Workbench',
    icon: 'IT',
    title: 'Image Tagger',
    description: 'Annotate images, inspect attributes, and export training data.',
    envKey: 'VITE_TAGGER_UI_URL',
    component: ImageTagger,
  },
  {
    id: 'article',
    label: 'Evidence',
    meta: 'Article Eater',
    icon: 'AE',
    title: 'Article Eater',
    description: 'Extract findings, generate rules, and manage evidence runs.',
    envKey: 'VITE_ARTICLE_UI_URL',
    component: ArticleEater,
  },
  {
    id: 'graph',
    label: 'Knowledge Graph',
    meta: 'Graph Explorer',
    icon: 'KG',
    title: 'Knowledge Graph',
    description: 'Explore causal links and evidence provenance.',
    envKey: 'VITE_GRAPH_UI_URL',
    component: KnowledgeGraph,
  },
];

function useModuleUrls() {
  const gateway = import.meta.env.VITE_GATEWAY_URL || window.location.origin;
  const defaults = {
    graphical: `${gateway}/graphical/`,
    tagger: `${gateway}/tagger/`,
    article: `${gateway}/article/`,
    graph: `${gateway}/graph/`,
  };

  return useMemo(() => {
    return moduleConfigs.reduce((acc, module) => {
      const value = import.meta.env[module.envKey] || defaults[module.id] || '';
      acc[module.id] = value.trim();
      return acc;
    }, {});
  }, []);
}

export default function App() {
  const [activeId, setActiveId] = useState('graphical');
  const [isNavOpen, setIsNavOpen] = useState(false);
  const moduleUrls = useModuleUrls();
  const activeModule = moduleConfigs.find((module) => module.id === activeId);
  const ActiveComponent = activeModule?.component;
  const gateway = import.meta.env.VITE_GATEWAY_URL || window.location.origin;

  return (
    <div className="shell">
      <Navigation
        items={moduleConfigs}
        activeId={activeId}
        onSelect={(id) => {
          setActiveId(id);
          setIsNavOpen(false);
        }}
        isOpen={isNavOpen}
        onToggle={() => setIsNavOpen((open) => !open)}
        gateway={gateway}
      />
      <main className="shell-main">
        <header className="shell-header">
          <div>
            <div className="header-eyebrow">Unified Research Console</div>
            <h1>{activeModule?.title}</h1>
            <p>{activeModule?.description}</p>
          </div>
          <div className="header-card">
            <div className="header-card-row">
              <span>Gateway</span>
              <span className="mono">{gateway}</span>
            </div>
            <div className="header-card-row">
              <span>API Prefix</span>
              <span className="mono">/api/v1/{activeModule?.id}</span>
            </div>
            <div className="header-card-row">
              <span>Status</span>
              <span className="status-pill">Ready</span>
            </div>
          </div>
        </header>
        {activeModule && ActiveComponent && (
          <ActiveComponent url={moduleUrls[activeModule.id]} />
        )}
      </main>
    </div>
  );
}
