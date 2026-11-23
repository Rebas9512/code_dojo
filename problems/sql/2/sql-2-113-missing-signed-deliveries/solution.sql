SELECT s.shop FROM parcel_shops s
LEFT JOIN parcel_log p ON p.shop = s.shop AND p.state = 'signed'
WHERE p.parcel IS NULL;
