SELECT a.kit AS first_kit, b.kit AS second_kit, COUNT(DISTINCT a.shop) AS shops
FROM kit_uses a JOIN kit_uses b ON a.shop = b.shop AND a.kit < b.kit
GROUP BY a.kit, b.kit HAVING COUNT(DISTINCT a.shop) >= 3
ORDER BY shops DESC, first_kit, second_kit;
