UPDATE Invoice 
SET delivery_status='$status', manager_id='$manager', driver_id='$driver', transport_id='$transport' 
WHERE id='$id';