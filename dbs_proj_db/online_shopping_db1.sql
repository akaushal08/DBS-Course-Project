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
