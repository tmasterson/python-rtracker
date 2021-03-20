-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS items;
CREATE TABLE items (
  item_id TEXT UNIQUE NOT NULL,
  location TEXT
);
