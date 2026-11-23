SELECT b.badge, IFNULL(e.dial, 'unrouted') AS dial
FROM binders b LEFT JOIN extensions e ON e.badge = b.badge;
