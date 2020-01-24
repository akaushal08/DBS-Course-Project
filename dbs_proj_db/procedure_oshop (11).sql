CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_cart`(

IN cid VARCHAR(10), in amount float,in uid varchar(10)
)

BEGIN

insert into cart values(cid,amount,uid);

END


CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_cart_items`(cid varchar(10),iid varchar(10),quant int, OUT stat int )

BEGIN

DECLARE var1 float;
DECLARE var2 float;

if(select qty from products where item_id=iid) < quant then

set stat:=0;

else
select item_price into var1 from products where item_id=iid;

if(select qty from cart_items where cart_id=cid and item_id=iid) is Null then
insert into cart_items values(cid,iid,quant);
else
update cart_items set qty=qty+quant where cart_id=cid and item_id=iid;
end if;

update cart set total_price=total_price+var1*quant where cart_id=cid;

update products set qty=qty-quant where item_id=iid;

set stat:=1;

end if;

END


CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_payment`(oidx varchar(10),pid varchar(10),uid varchar(10), OUT  stat1 int )


BEGIN

declare var1 float;

select total_price into var1
from cart
where user_id=uid;

if var1=0.0 then

set stat1:=0;

else

insert into payment values (pid,var1,'cod',uid);
commit;
insert into orders values (oidx,var1,pid);

set stat1:= 1;
end if;

END



CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_orderitems`( in oid varchar(10),in cid varchar(10),OUT stat int)

BEGIN

declare var1 varchar(10);

declare var2 varchar(10);

declare var3 int;

DECLARE exit_loop BOOLEAN;
declare cur

cursor for

select * from cart_items where cart_id=cid ;

DECLARE CONTINUE HANDLER FOR NOT FOUND SET exit_loop = TRUE;

open cur;

order_items_loop:LOOP

fetch cur into var1,var2,var3;
IF exit_loop THEN

       CLOSE cur;

       LEAVE order_items_loop;

end if;

insert into order_items values(oid,var2,var3);
delete from cart_items where cart_id=cid and item_id=var2;
update cart set total_price=0.0 where cart_id=cid;

set stat:=1;



end loop
 order_items_loop;


END







CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_cart_items`(cid varchar(10),iid varchar(10),OUT stat int )
BEGIN

DECLARE var1 float;
DECLARE var2 float;
DECLARE cnt int;


if(select qty from cart_items where item_id=iid and cart_id=cid) is Null then

set stat:=0;

else

select item_price into var1 from products where item_id=iid;

update cart_items set qty=qty-1 where cart_id=cid and item_id=iid;

select qty into cnt from cart_items where cart_id=cid and item_id=iid;
if cnt = 0 then
delete from cart_items where cart_id=cid and item_id=iid;
end if;
update cart set total_price=total_price-var1 where cart_id=cid;
update products set qty=qty+1 where item_id=iid;
set stat:=1;
end if;


END
