SELECT title, category, price
FROM books
WHERE (category = 'fantasy' OR category = 'scifi') AND price < 35;
