CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256)
);

CREATE TABLE poll (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    creator_id INTEGER NOT NULL REFERENCES "user"(id)
);

CREATE TABLE option (
    id SERIAL PRIMARY KEY,
    text VARCHAR(200) NOT NULL,
    poll_id INTEGER NOT NULL REFERENCES poll(id)
);

CREATE TABLE vote (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER NOT NULL REFERENCES poll(id),
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    choice_id INTEGER NOT NULL REFERENCES option(id)
);
