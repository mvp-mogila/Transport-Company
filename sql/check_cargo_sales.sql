SELECT Detalization.id
FROM Detalization
JOIN Invoice I ON Detalization.invoice_id = I.id
JOIN Cargo C ON Detalization.cargo_id = C.id
WHERE C.name = '$cargo_name'
AND I.delivery_status != 'Отменен'
AND YEAR(I.send_date) = '$year'
AND MONTH(I.send_date) = '$month'; 