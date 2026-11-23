SELECT m.name FROM makers m
WHERE m.maker NOT IN (SELECT i.maker FROM ink_orders i WHERE i.pigment = 'red');
