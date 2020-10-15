-- drop existing table
DROP TABLE IF EXISTS comments;

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


.import rubber_comparison_output_dedup.csv comments
.headers off
DELETE FROM comments WHERE aspect='aspect';
SELECT COUNT(*) from comments;

