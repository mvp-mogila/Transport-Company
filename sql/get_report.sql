SELECT Report.*, C.name AS cargo_name 
FROM Report JOIN Cargo C ON Report.cargo_id = C.id
WHERE C.name LIKE '$cargo_name'
AND Report.year LIKE '$year'
AND Report.month LIKE '$month';