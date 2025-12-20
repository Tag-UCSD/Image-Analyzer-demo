-- Knowledge Graph schema tables

CREATE TABLE IF NOT EXISTS graph.nodes (
    node_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_key VARCHAR(120) NOT NULL,
    label VARCHAR(255) NOT NULL,
    level VARCHAR(50) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_graph_nodes_key
    ON graph.nodes (node_key);

CREATE TABLE IF NOT EXISTS graph.edges (
    edge_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_node VARCHAR(120) NOT NULL,
    to_node VARCHAR(120) NOT NULL,
    status VARCHAR(50) DEFAULT 'hypothesized',
    param JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_graph_edges_from
    ON graph.edges (from_node);

CREATE INDEX IF NOT EXISTS idx_graph_edges_to
    ON graph.edges (to_node);

CREATE TABLE IF NOT EXISTS graph.edge_evidence (
    evidence_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    edge_id UUID,
    source_id UUID,
    summary TEXT,
    effect_direction VARCHAR(50),
    effect_size DOUBLE PRECISION,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
