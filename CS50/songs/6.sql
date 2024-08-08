SELECT name FROM songs WHERE id = (SELECT id FROM artists WHERE name = 'Post Malone');
