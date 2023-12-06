SELECT * 
FROM Invoice JOIN Client C ON Invoice.client_id = C.doc_num JOIN User CU ON C.user_id = CU.id
WHERE CU.id='$user_id'
AND Invoice.id LIKE '$delivery_id'
AND Invoice.total_weight>='$weight_lower' AND Invoice.total_weight<='$weight_upper'
AND Invoice.delivery_status LIKE '$status'
ORDER BY Invoice.creation_date;