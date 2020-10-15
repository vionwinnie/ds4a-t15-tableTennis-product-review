-- NOTE: to execute: sqlite>.read dbInit.sql
-- Setup
.header on
.mode list
.separator ','

-- drop existing table
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS rubbers;

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


.separator "|"
-- define table
CREATE TABLE comments (
    ID INT,
    COMMENT_ID TEXT,
    COMMENT_TEXT TEXT,
    ENTITY1 TEXT,
    ENTITY2 TEXT,
    ASPECT TEXT,
    DIRECTION TEXT
);

.tables

.import rubber_comparison_output_fixed2.csv comments
.headers off
DELETE FROM comments WHERE aspect='aspect';
SELECT COUNT(*) from comments;


-- IMPORT DATA
.separator ","
.import revspin_rubber_list.csv rubbers
.headers off
DELETE FROM rubbers WHERE name='name';
SELECT COUNT(*) from rubbers;


