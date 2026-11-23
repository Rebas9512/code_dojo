SELECT b.given, b.family, m.room, m.wing
FROM binders b LEFT JOIN desk_map m ON m.badge = b.badge;
