CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,

    source VARCHAR(100) NOT NULL,
    source_job_id VARCHAR(255),

    title TEXT NOT NULL,
    company TEXT NOT NULL,
    company_logo TEXT,
    location TEXT,

    description TEXT,
    url TEXT NOT NULL,

    posted_at TIMESTAMP,
    discovered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    experience_level VARCHAR(100),
    employment_type VARCHAR(100),
    remote_type VARCHAR(100),

    salary_min NUMERIC,
    salary_max NUMERIC,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source, source_job_id)
);

CREATE INDEX IF NOT EXISTS idx_jobs_posted_at
ON jobs(posted_at);

CREATE INDEX IF NOT EXISTS idx_jobs_source
ON jobs(source);

CREATE INDEX IF NOT EXISTS idx_jobs_title
ON jobs(title);