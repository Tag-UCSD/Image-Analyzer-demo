import React from 'react';

import ModuleFrame from '../components/ModuleFrame.jsx';

export default function ImageTagger({ url }) {
  return (
    <ModuleFrame
      title="Image Tagger"
      description="Annotate images, inspect attributes, and export training data."
      url={url}
      envKey="VITE_TAGGER_UI_URL"
    />
  );
}
