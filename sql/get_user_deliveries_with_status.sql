SELECT * 
FROM Invoice JOIN Client ON Invoice.client_id = Client.doc_num JOIN User ON Client.user_id = User.id
WHERE user_id='$user_id' 
AND send_date BETWEEN STR_TO_DATE('$send_date', "%d-%m-%Y") AND STR_TO_DATE('$delivery_date', "%d-%m-%Y")
AND total_weight>='$weight_lower' AND total_weight<='$weight_upper'
AND delivery_status='$status';