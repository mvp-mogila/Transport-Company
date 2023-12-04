SELECT * 
FROM Invoice 
JOIN Client ON Invoice.client_id = Client.doc_num
JOIN Staff ON Invoice.manager_id = Staff.id
JOIN Staff ON Invoice.driver_id = Staff.id
JOIN Transport ON Invoice.transport_id = Transport.id
WHERE send_date=STR_TO_DATE('$send_date', "%d-%m-%Y") AND delivery_date=STR_TO_DATE('$delivery_date', "%d-%m-%Y");