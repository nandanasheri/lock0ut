DROP TABLE IF EXISTS states;

CREATE TABLE activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    abbreviation TEXT NOT NULL
);