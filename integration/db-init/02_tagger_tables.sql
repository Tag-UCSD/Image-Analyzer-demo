-- Image Tagger schema tables

CREATE TABLE IF NOT EXISTS tagger.raters (
    rater_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    display_name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'rater',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tagger.attributes (
    attribute_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID,
    attribute_name VARCHAR(120) NOT NULL,
    value DOUBLE PRECISION,
    confidence DOUBLE PRECISION,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tagger_attributes_image
    ON tagger.attributes (image_id);

CREATE TABLE IF NOT EXISTS tagger.tags (
    tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    image_id UUID,
    tag_name VARCHAR(120) NOT NULL,
    category VARCHAR(120),
    value VARCHAR(255),
    rater_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tagger_tags_image
    ON tagger.tags (image_id);
