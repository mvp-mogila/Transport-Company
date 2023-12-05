SELECT * FROM Invoice JOIN Client ON invoice.client_id=Client.doc_num
WHERE Invoice.id='$id' AND Invoice.client_id='$client_id';