SELECT paper, SUM(CASE WHEN side = 'sell' THEN coins ELSE -coins END) AS gain
FROM paper_trades
GROUP BY paper;
