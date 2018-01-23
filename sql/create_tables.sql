CREATE TABLE IF NOT EXISTS Account (
/*  column          type            nullability     constraints  */
    id              SERIAL          /* NEVER */     PRIMARY KEY,
    username        TEXT            NOT NULL        UNIQUE,
    password        CHARACTER(60)   NOT NULL,
    display_name    TEXT,
    admin           BOOLEAN         NOT NULL        DEFAULT FALSE,

/*  additional constraints          rule  */
    CONSTRAINT username_length      CHECK (1 <= LENGTH(username) AND LENGTH(username) <= 16),       -- Constrain username length.
    CONSTRAINT username_format      CHECK (username ~ '^[0-9a-z]*$'),                               -- Allow only lowercase alphanumeric usernames.
    CONSTRAINT password_length      CHECK (LENGTH(password) = 60),                                  -- Hash in bcrypt is guaranteed to be 60 characters.
    CONSTRAINT display_name_length  CHECK (LENGTH(display_name) <= 50)                              -- Constrain display name length.
);

CREATE TABLE IF NOT EXISTS Tag (
/*  column          type            nullability     constraints  */
    id              SERIAL          /* NEVER */     PRIMARY KEY,
    title           TEXT            NOT NULL        UNIQUE,

/*  additional constraints          rule  */
    CONSTRAINT title_length         CHECK (1 <= LENGTH(title) AND LENGTH(title) <= 16)              -- Constrain title length.
);

CREATE TABLE IF NOT EXISTS Thread (
/*  column          type            nullability     constraints  */
    id              SERIAL          /* NEVER */     PRIMARY KEY,
    author_id       INTEGER         NOT NULL        REFERENCES Account(id),
    title           TEXT            NOT NULL,
    created         TIMESTAMP       NOT NULL        DEFAULT (NOW() AT TIME ZONE 'UTC'),

/*  additional constraints          rule  */
    CONSTRAINT title_length         CHECK (10 <= LENGTH(title) AND LENGTH(title) <= 80)             -- Constrain title length.
);

CREATE TABLE IF NOT EXISTS Response (
/*  column          type            nullability     constraints  */
    id              SERIAL          /* NEVER */     PRIMARY KEY,
    author_id       INTEGER         NOT NULL        REFERENCES Account(id),
    thread_id       INTEGER         NOT NULL        REFERENCES Thread(id)       ON DELETE CASCADE,
    content         TEXT            NOT NULL,
    created         TIMESTAMP       NOT NULL        DEFAULT (NOW() AT TIME ZONE 'UTC'),
    
/*  additional constraints          rule  */
    CONSTRAINT content_length       CHECK (10 <= LENGTH(content) AND LENGTH(content) <= 1000)       -- Constrain content length.
);

CREATE TABLE IF NOT EXISTS ThreadTag (
/*  column          type            nullability     constraints  */
    tag_id          INTEGER         NOT NULL        REFERENCES Tag(id)          ON DELETE CASCADE,
    thread_id       INTEGER         NOT NULL        REFERENCES Thread(id)       ON DELETE CASCADE,

/*  additional constraints          rule  */
    CONSTRAINT no_duplicates        UNIQUE(tag_id, thread_id)                                       -- Disallow duplicates.
);
