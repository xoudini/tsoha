INSERT INTO Account (username, password, admin) VALUES ('dan', '$2b$12$HrMmPp9aWiywl/aqAYzRDO9LySiSGGygD.Pta2P8SCFb2OnNA8x1e', TRUE);
INSERT INTO Account (username, password, admin) VALUES ('test', '$2b$12$4cIZeUPBt2yjH4bN6Zigfebnc8R.PliSvbCUNdc9Bna1e5FWbkHNa', FALSE);
INSERT INTO Profile (account_id, display_name) VALUES (1, 'Dan L');
INSERT INTO Profile (account_id, display_name) VALUES (2, 'Test User');
INSERT INTO Tag (title) VALUES ('discussion');
INSERT INTO Tag (title) VALUES ('meta');
INSERT INTO Tag (title) VALUES ('suggestion');
INSERT INTO Tag (title) VALUES ('programming');
INSERT INTO Thread (author_id, title, created) VALUES (1, 'First post, ignore.', now() AT TIME ZONE 'utc');
INSERT INTO Response (author_id, thread_id, content, created) VALUES (1, 1, 'Read the title.', now() AT TIME ZONE 'utc');
INSERT INTO Response (author_id, thread_id, content, created) VALUES (2, 1, '<ignoring>', now() AT TIME ZONE 'utc');
INSERT INTO Thread (author_id, title, created) VALUES (1, 'Add more tags.', now() AT TIME ZONE 'utc');
INSERT INTO Response (author_id, thread_id, content, created) VALUES (1, 2, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', now() AT TIME ZONE 'utc');
INSERT INTO ThreadTag (tag_id, thread_id) VALUES (2, 2);
INSERT INTO ThreadTag (tag_id, thread_id) VALUES (3, 2);
