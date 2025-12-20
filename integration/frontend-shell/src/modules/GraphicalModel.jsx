import React from 'react';

import ModuleFrame from '../components/ModuleFrame.jsx';

export default function GraphicalModel({ url }) {
  return (
    <ModuleFrame
      title="Graphical Model"
      description="Bayesian inference, interventions, and prediction outputs."
      url={url}
      envKey="VITE_GRAPHICAL_UI_URL"
    />
  );
}
