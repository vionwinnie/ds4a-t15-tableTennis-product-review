-- NOTE: to execute: sqlite>.read dbInit.sql
-- Setup
.header on
.mode list
.separator ','

-- Define table schema

CREATE TABLE rubbers (
   NAME TEXT,
   SPEED DECIMAL(6,2),
   SPIN DECIMAL(6,2),
   TACKINESS DECIMAL(6,2),
   OVERALL DECIMAL(6,2),
   PRICE DECIMAL(6,2),
   RATINGS INT,
   BRAND TEXT
);

CREATE TABLE comments (
   COMMENT_ID INT,
   COMMENT_TEXT TEXT,
   ENTITY1 TEXT,
   ENTITY2 TEXT,
   ASPECT TEXT,
   DIRECTION TEXT
);

.tables

-- IMPORT DATA
.separator ","
.import revspin_rubber_list.csv rubbers
.headers off
SELECT COUNT(*) from rubbers;


