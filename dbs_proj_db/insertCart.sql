CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_cart`(
IN cid VARCHAR(10), in amount float,in uid varchar(10)
)
BEGIN
insert into cart values(cid,amount,uid);
END