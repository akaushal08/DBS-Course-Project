create table user (user_id varchar(10), name varchar(50),
  address varchar(60), gender varchar(10), phone_no varchar(10), email_id varchar(40), password varchar(15),
  primary key (user_id));


create table category (category_id varchar(10), category_name varchar(40), primary key (category_id));


create table products (item_id varchar(10), item_name varchar(40), item_price float, qty int, category_id varchar(10),
  primary key(item_id), foreign key (category_id) references category(category_id));


create table cart (cart_id varchar(10), total_price float,
  user_id varchar(10), primary key (cart_id),
  foreign key (user_id) references user(user_id));


create table cart_items(cart_id varchar(10), item_id varchar(10), qty int,
  primary key (cart_id,item_id), foreign key (cart_id) references cart(cart_id),
  foreign key (item_id) references products(item_id));


create table payment(transaction_id varchar(10), amount float, mode_of_pay varchar(20), user_id varchar(10),
  primary key(transaction_id), foreign key (user_id) references user(user_id));


create table orders (order_id varchar(10), order_amt float,
  transaction_id varchar(10), primary key(order_id),
  foreign key (transaction_id) references payment(transaction_id));


create table order_items(order_id varchar(10), item_id varchar(10), qty int,
  primary key (order_id,item_id), foreign key (order_id) references orders(order_id),
  foreign key (item_id) references products(item_id));


create table area_detail(area_code varchar(10), area_name varchar(20), primary key(area_code));


create table employee (employee_id varchar(10), name varchar(50),
  address varchar(60), gender varchar(10), phone_no varchar(10), email_id varchar(40), password varchar(15),
  salary float, area_code varchar(10), primary key (employee_id),
  foreign key (area_code) references area_detail(area_code));


create table shipment (order_id varchar(10), area_code varchar(10),
odate date, primary key (order_id), foreign key (area_code) references area_detail(area_code),
foreign key (order_id) references orders(order_id));


create table reviews(review_id varchar(10), item_id varchar(10), rating float,
primary key(review_id),foreign key (item_id) references products(item_id));


insert into category values('C300','Clothing'),('C100','Grocery'),('C200','Electrical');
insert into products values('P100','FruitBasket',100.0,10,'C100'),('P101','Onions',10.0,100,'C100'),('P102','Tomato',5.0,100,'C100'),('P103','Potato',4.0,100,'C100'),
('P104','Apples',25.0,100,'C100'),('P105','Banana',4.0,100,'C100');
insert into products values('P200','Wires',20.0,50,'C200'),('P201','Socket',150.0,20,'C200'),('P202','Lamp',200.0,10,'C200'),('P203','SoundSytsem',2000.0,5,'C200'),
('P204','Bulbs',50.0,20,'C200');
insert into products values('P300','Tshirts',500.0,25,'C300'),('P301','Jeans',800.0,20,'C300'),('P302','Sweaters',700.0,15,'C300'),('P303','Shirts',850.0,15,'C300'),
('P304','Jackets',1000.0,10,'C300');


insert into area_detail values('A100','Manipal'),('A101','Udupi'),('A102','Mangalore'),('A103','Bangalore'),('A104','Bagalkot'),('A105','Haveri'),('A106','Koppal');

/*insert into employee values(E100,Akshay,Bl21/R04/576104,Male,9234267867,akshay@gmail.com,employee100,10000,A100),
(E101,Bhavika,B21/R12/576103,Female,9234267867,bhavika@gmail.com,employee101,9000,A101),
(E102,Jeff,B1/R24/576105,Male,9234267867,jeff@gmail.com,employee102,10000,A102),
(E103,Kartik,Bl3/R40/576106,Male,9234267867,kartik@gmail.com,employee103,7000,A103),
(E104,Shreya,B23/R54/576101,Female,9234267867,shreya@gmail.com,employee104,10000,A104),
(E105,Shubham,B34/R78/57610,Male,9234267867,shubham@gmail.com,employee105,9000,A105),
(E106,Vishu,B45/R23/576123,Male,9234267867,vishu@gmail.com,employee106,8000,A106);*/
