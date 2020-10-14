.separator "|"
.import dummy_comments.csv comments
.headers off
DELETE FROM comments WHERE aspect='aspect';
SELECT COUNT(*) from comments;

