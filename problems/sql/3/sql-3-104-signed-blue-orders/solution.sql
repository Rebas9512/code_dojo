SELECT m.maker FROM makers m
WHERE EXISTS (SELECT 1 FROM ink_orders i WHERE i.maker = m.maker AND i.pigment = 'blue');
