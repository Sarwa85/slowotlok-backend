DROP TABLE IF EXISTS cards;

CREATE TABLE cards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT UNIQUE NOT NULL,
  tr TEXT NOT NULL
);

DROP TABLE IF EXISTS scores;

CREATE TABLE scores (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  card_id INTEGER UNIQUE NOT NULL,
  good INTEGER NOT NULL,
  bad INTEGER NOT NULL
);