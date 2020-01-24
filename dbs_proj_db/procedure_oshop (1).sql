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


CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_payment`(oid varchar(10),pid varchar(10),uid varchar(10), OUT  stat1 int )


BEGIN

declare var1 float;

select total_price into var1
from cart
where user_id=uid;

if var1=0.0 then

set stat1=0;

else

insert into payment values (pid,var1,'cod',uid);

insert into orders values (oid,var1,pid);

set stat1= 1;
end if;

END
