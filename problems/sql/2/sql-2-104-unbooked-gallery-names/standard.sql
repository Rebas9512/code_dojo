SELECT g.name
FROM gallery_list g
LEFT JOIN hang_log h ON h.gallery = g.gallery
WHERE h.slip IS NULL;
