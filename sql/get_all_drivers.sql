SELECT Staff.id AS id, User.surname AS surname
FROM Staff JOIN User ON Staff.user_id = User.id
WHERE position='Водитель';