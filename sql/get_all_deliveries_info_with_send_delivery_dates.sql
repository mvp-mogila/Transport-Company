SELECT Invoice.*,
C.doc_num AS client_id, CU.surname AS client_surname,
MU.surname AS manager_surname,
DU.surname AS driver_surname,
T.model AS transport_model
FROM Invoice 
JOIN Client C ON Invoice.client_id = C.doc_num JOIN User CU ON C.user_id = CU.id
LEFT JOIN Staff M ON Invoice.manager_id = M.id LEFT JOIN User MU ON M.user_id = MU.id
LEFT JOIN Staff D ON Invoice.driver_id = D.id LEFT JOIN User DU ON D.user_id = DU.id
LEFT JOIN Transport T ON Invoice.transport_id = T.id
WHERE Invoice.id LIKE '$delivery_id'
AND Invoice.send_date = STR_TO_DATE('$send_date', "%Y-%m-%d")
AND Invoice.delivery_date = STR_TO_DATE('$delivery_date', "%Y-%m-%d")
AND Invoice.delivery_status LIKE '$status'
ORDER BY Invoice.creation_date;