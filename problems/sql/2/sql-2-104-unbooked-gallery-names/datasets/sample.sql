CREATE TABLE gallery_list (gallery integer, name text);
INSERT INTO gallery_list VALUES
    (4, 'Fern'),
    (8, 'Yew'),
    (12, 'Oak');

CREATE TABLE hang_log (slip integer, gallery integer, title text);
INSERT INTO hang_log VALUES
    (91, 4, NULL),
    (92, 12, 'Tide'),
    (93, 4, 'Rain');
