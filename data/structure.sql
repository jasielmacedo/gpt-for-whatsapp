CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    user_message TEXT NOT NULL,
    ai_reply TEXT NOT NULL
);