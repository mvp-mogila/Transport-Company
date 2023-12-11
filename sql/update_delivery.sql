UPDATE Invoice 
SET delivery_status='В работе', manager_id='$manager', driver_id='$driver', transport_id='$transport' 
WHERE id='$id';