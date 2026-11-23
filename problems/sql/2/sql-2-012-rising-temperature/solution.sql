SELECT today.log_id
FROM weather today
JOIN weather prev ON today.day = prev.day + 1
WHERE today.degrees > prev.degrees;
