-- Article Eater schema tables

CREATE TABLE IF NOT EXISTS evidence.articles (
    article_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID,
    processing_status VARCHAR(50) DEFAULT 'pending',
    l0_completed_at TIMESTAMP,
    l2_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence.findings (
    finding_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    article_id UUID,
    finding_text TEXT NOT NULL,
    effect_direction VARCHAR(50),
    effect_size DOUBLE PRECISION,
    p_value DOUBLE PRECISION,
    confidence_interval JSONB DEFAULT '{}'::jsonb,
    population TEXT,
    design VARCHAR(100),
    quality VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_evidence_findings_article
    ON evidence.findings (article_id);

CREATE TABLE IF NOT EXISTS evidence.rules (
    rule_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_text TEXT NOT NULL,
    confidence DOUBLE PRECISION,
    triangulation_score DOUBLE PRECISION,
    contradiction_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence.rule_evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    rule_id UUID,
    finding_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
