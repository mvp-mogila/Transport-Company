SELECT COUNT(id) AS total_deliveries 
FROM Invoice JOIN Client ON Invoice.client_id=Client.doc_num
WHERE client_id='$client_id';