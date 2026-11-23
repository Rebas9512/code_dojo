SELECT p.node,
       CASE
           WHEN p.parent IS NULL THEN 'root'
           WHEN EXISTS (
               SELECT 1
               FROM collection_nodes child
               WHERE child.parent = p.node
           ) THEN 'branch'
           ELSE 'leaf'
       END AS role
FROM collection_nodes p;
