UPDATE print_faces
SET face = CASE WHEN face = 'recto' THEN 'verso' ELSE 'recto' END;
