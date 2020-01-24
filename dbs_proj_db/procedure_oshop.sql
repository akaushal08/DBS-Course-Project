CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_cart`(
IN cid VARCHAR(10), in amount float,in uid varchar(10)
)
BEGIN
insert into cart values(cid,amount,uid);
END


CREATE DEFINER=`root`@`localhost` FUNCTION `insert_cart_items`(cid varchar(10),iid varchar(10),quant int) RETURNS int(11)
BEGIN
DECLARE var1 float;
if(select qty from products where item_id=iid) < quant then
RETURN 0;
else
select item_price into var1 from products where item_id=iid;
insert into cart_items values(cid,iid,quant);
update cart set total_price=var1*quant where cart_id=cid;
update products set qty=qty-quant where item_id=iid;
RETURN 1;
end if;
END
