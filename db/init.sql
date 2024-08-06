CREATE TABLE IF NOT EXISTS reddit_posts (
    id SERIAL PRIMARY KEY,
    headline VARCHAR(255),
    content TEXT,
    url VARCHAR(255),
    created_at TIMESTAMP,
    rating FLOAT,
    llm_evaluation JSONB
);