SELECT paper, 'east' AS counter, east AS price FROM quote_board WHERE east IS NOT NULL
UNION ALL
SELECT paper, 'west', west FROM quote_board WHERE west IS NOT NULL
UNION ALL
SELECT paper, 'pier', pier FROM quote_board WHERE pier IS NOT NULL;
