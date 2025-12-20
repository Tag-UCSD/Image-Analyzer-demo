-- Shared core schema tables

CREATE TABLE IF NOT EXISTS core.users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE TABLE IF NOT EXISTS core.images (
    image_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(500) NOT NULL,
    space_type VARCHAR(100),
    source VARCHAR(255),
    uploaded_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_core_images_space_type
    ON core.images (space_type);

CREATE TABLE IF NOT EXISTS core.literature_sources (
    source_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doi VARCHAR(255) UNIQUE,
    title TEXT NOT NULL,
    authors JSONB,
    year INTEGER,
    venue VARCHAR(255),
    abstract TEXT,
    citation_count INTEGER DEFAULT 0,
    full_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_core_literature_year
    ON core.literature_sources (year);

-- Foreign key constraints (added defensively to allow idempotent runs)
DO $$
BEGIN
    ALTER TABLE core.images
        ADD CONSTRAINT fk_core_images_user
        FOREIGN KEY (uploaded_by) REFERENCES core.users(user_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE tagger.raters
        ADD CONSTRAINT fk_tagger_raters_user
        FOREIGN KEY (user_id) REFERENCES core.users(user_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE tagger.attributes
        ADD CONSTRAINT fk_tagger_attributes_image
        FOREIGN KEY (image_id) REFERENCES core.images(image_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE tagger.tags
        ADD CONSTRAINT fk_tagger_tags_image
        FOREIGN KEY (image_id) REFERENCES core.images(image_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE tagger.tags
        ADD CONSTRAINT fk_tagger_tags_rater
        FOREIGN KEY (rater_id) REFERENCES tagger.raters(rater_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE evidence.articles
        ADD CONSTRAINT fk_evidence_articles_source
        FOREIGN KEY (source_id) REFERENCES core.literature_sources(source_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE evidence.findings
        ADD CONSTRAINT fk_evidence_findings_article
        FOREIGN KEY (article_id) REFERENCES evidence.articles(article_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE evidence.rule_evidence
        ADD CONSTRAINT fk_evidence_rule_evidence_rule
        FOREIGN KEY (rule_id) REFERENCES evidence.rules(rule_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE evidence.rule_evidence
        ADD CONSTRAINT fk_evidence_rule_evidence_finding
        FOREIGN KEY (finding_id) REFERENCES evidence.findings(finding_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE graphical.predictions
        ADD CONSTRAINT fk_graphical_predictions_model_run
        FOREIGN KEY (model_run_id) REFERENCES graphical.model_runs(model_run_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE graphical.predictions
        ADD CONSTRAINT fk_graphical_predictions_image
        FOREIGN KEY (image_id) REFERENCES core.images(image_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE graph.edge_evidence
        ADD CONSTRAINT fk_graph_edge_evidence_edge
        FOREIGN KEY (edge_id) REFERENCES graph.edges(edge_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE graph.edge_evidence
        ADD CONSTRAINT fk_graph_edge_evidence_source
        FOREIGN KEY (source_id) REFERENCES core.literature_sources(source_id);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;
