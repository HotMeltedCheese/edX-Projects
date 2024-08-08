SELECT AVG(energy) FROM songs WHERE id = (SELECT id FROM artists WHERE name = 'drake');
