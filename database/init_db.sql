-- Create the database and user
CREATE DATABASE iris_chatbot_db;
CREATE USER iris_chatbot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE iris_chatbot_db TO iris_chatbot_user;

-- Connect to iris_chatbot_db and create tables
\c iris_chatbot_db;

CREATE TABLE prompts (
    id SERIAL PRIMARY KEY,
    prompt_text TEXT NOT NULL,
    reference TEXT
);

CREATE TABLE user_interactions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    user_input TEXT,
    bot_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_feedback (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    interaction_id INTEGER REFERENCES user_interactions(id),
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE iris (
    filename TEXT PRIMARY KEY,
    content TEXT
);
