SELECT * 
FROM Invoice JOIN Client ON Invoice.client_id = Client.doc_num JOIN User ON Client.user_id = User.id
WHERE user_id='$user_id';