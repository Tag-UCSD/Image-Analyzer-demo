import React from 'react';

import ModuleFrame from '../components/ModuleFrame.jsx';

export default function ArticleEater({ url }) {
  return (
    <ModuleFrame
      title="Article Eater"
      description="Extract findings, generate rules, and manage evidence runs."
      url={url}
      envKey="VITE_ARTICLE_UI_URL"
    />
  );
}
