import React from 'react';

import ModuleFrame from '../components/ModuleFrame.jsx';

export default function KnowledgeGraph({ url }) {
  return (
    <ModuleFrame
      title="Knowledge Graph"
      description="Explore causal links and evidence provenance."
      url={url}
      envKey="VITE_GRAPH_UI_URL"
    />
  );
}
