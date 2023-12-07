USE TransportCompany;

CREATE DEFINER=`admin`@`localhost` PROCEDURE `create_report`(in cargo_name VARCHAR(50), in rep_year INT, in rep_month INT)

BEGIN
DECLARE done INT default 0;
DECLARE total_amount INT default 0;
DECLARE cargo_id INT default 0;

DECLARE C1 CURSOR FOR
SELECT D.cargo_id, SUM(D.cargo_amount)
FROM Detalization D
JOIN Cargo C ON D.cargo_id = C.id
JOIN Invoice I ON D.invoice_id = I.id
WHERE I.delivery_status != 'Отменен'
AND C.name = cargo_name
AND YEAR(I.send_date) = rep_year
AND MONTH(I.send_date) = rep_month
GROUP BY D.cargo_id;

DECLARE EXIT HANDLER FOR NOT FOUND SET done = 1;
OPEN C1;
WHILE done = 0 DO
FETCH C1 INTO cargo_id, total_amount;
INSERT INTO `Report`(`year`, `month`, `cargo_id`, `amount`) VALUES(rep_year, rep_month, cargo_id, total_amount);
END WHILE;
CLOSE C1;

END

DROP PROCEDURE create_report ;