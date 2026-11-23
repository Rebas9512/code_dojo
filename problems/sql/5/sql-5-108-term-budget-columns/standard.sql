SELECT desk, MAX(coins) FILTER (WHERE term = 'dawn') AS dawn,
       MAX(coins) FILTER (WHERE term = 'noon') AS noon,
       MAX(coins) FILTER (WHERE term = 'dusk') AS dusk
FROM term_grants
GROUP BY desk;
