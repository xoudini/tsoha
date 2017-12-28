CREATE TABLE IF NOT EXISTS Account (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin BOOLEAN
);

CREATE TABLE IF NOT EXISTS Profile (
    account_id INTEGER REFERENCES Account(id),
    display_name TEXT
);

CREATE TABLE IF NOT EXISTS Tag (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Thread (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES Account(id),
    title TEXT NOT NULL,
    created TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS Response (
    id SERIAL PRIMARY KEY,
    author_id INTEGER REFERENCES Account(id),
    thread_id INTEGER REFERENCES Thread(id),
    content TEXT NOT NULL,
    created TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS ThreadTag (
    tag_id INTEGER REFERENCES Tag(id),
    thread_id INTEGER REFERENCES Thread(id),
    UNIQUE(tag_id, thread_id)
);
