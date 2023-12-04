SELECT Invoice.*, C.doc_num AS client_id, MU.surname AS manager_surname, DU.surname AS driver_surname, T.model AS transport_model
FROM Invoice 
JOIN Client C ON Invoice.client_id = C.doc_num
JOIN Staff M ON Invoice.manager_id = M.id JOIN User MU ON M.user_id = MU.id
JOIN Staff D ON Invoice.driver_id = D.id JOIN User DU ON D.user_id = DU.id
JOIN Transport T ON Invoice.transport_id = T.id
WHERE Invoice.send_date=STR_TO_DATE('$send_date', "%d-%m-%Y")
AND Invoice.delivery_status='$status';