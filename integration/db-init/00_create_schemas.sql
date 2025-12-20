-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- Create schemas for each module
CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS tagger;
CREATE SCHEMA IF NOT EXISTS evidence;
CREATE SCHEMA IF NOT EXISTS graphical;
CREATE SCHEMA IF NOT EXISTS graph;

-- Set default search path for the database
ALTER DATABASE image_analyzer SET search_path TO core, tagger, evidence, graphical, graph, public;
