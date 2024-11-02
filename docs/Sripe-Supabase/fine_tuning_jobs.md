create table fine_tuning_jobs (
    id uuid primary key default uuid_generate_v4(),
    user_email text not null,
    job_id text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null,
    hyperparameters jsonb not null
    ADD COLUMN is_public boolean DEFAULT true;
    ADD COLUMN description text;
);