-- Graphical Model schema tables

CREATE TABLE IF NOT EXISTS graphical.model_runs (
    model_run_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name VARCHAR(120) NOT NULL,
    model_version VARCHAR(60) NOT NULL,
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    training_window VARCHAR(120),
    metrics JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS graphical.edge_priors (
    edge_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_node VARCHAR(120) NOT NULL,
    to_node VARCHAR(120) NOT NULL,
    prior_mean DOUBLE PRECISION NOT NULL,
    prior_sd DOUBLE PRECISION NOT NULL,
    source VARCHAR(120),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_graphical_edge_unique
    ON graphical.edge_priors (from_node, to_node);

CREATE TABLE IF NOT EXISTS graphical.predictions (
    prediction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_run_id UUID,
    image_id UUID,
    prediction_payload JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_graphical_predictions_image
    ON graphical.predictions (image_id);
