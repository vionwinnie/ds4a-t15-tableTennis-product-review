-- Remove hyphen from MXP-related comments
UPDATE comments
SET ENTITY1 = 'MXP'
WHERE
    COMMENT_ID in (4,5,6,7,14,15,16,17);

UPDATE comments
SET ENTITY2 = 'MXP'
WHERE
    COMMENT_ID in (8,9,19,18,19,20);

