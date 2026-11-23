SELECT press, MAX(observed) AS last_signal FROM press_signals
WHERE observed >= DATE '2025-01-01' AND observed <= DATE '2025-12-31'
GROUP BY press;
