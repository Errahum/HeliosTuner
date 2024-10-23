CREATE TABLE chat_histories (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    email text NOT NULL,
    user_message text NOT NULL,
    model text NOT NULL,
    max_tokens int NOT NULL,
    temperature float NOT NULL,
    stop text,
    response text NOT NULL,
    created_at timestamp DEFAULT current_timestamp
);