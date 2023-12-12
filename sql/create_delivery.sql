INSERT INTO Invoice(creation_date, send_date, delivery_date, send_address, delivery_address, client_id, delivery_status, total_weight)
VALUES (STR_TO_DATE('$creation_date', "%Y-%m-%d"),
STR_TO_DATE('$send_date', "%Y-%m-%d"),
STR_TO_DATE('$delivery_date', "%Y-%m-%d"),
'$send_address', '$delivery_address', '$client_id', 'В работе', '$total_weight');