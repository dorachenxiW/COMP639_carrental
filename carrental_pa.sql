
create table user (
userid INT NOT NULL auto_increment,
username varchar(255) NOT NULL,
firstname varchar(100),
lastname varchar(100),
password varchar(255) NOT NULL,
email varchar (100) NOT NULL,
catergory varchar(60),
primary key (userid)
);

create table car (
carid INT NOT NULL auto_increment,
numberplate varchar(100),
model varchar(255),
colour varchar(60),
year int,
status varchar(100),
rentalfee decimal(8,2),
primary key (carid)
);

create table customer (
customerid INT NOT NULL,
username varchar(100) NOT NULL,
password varchar(255) NOT NULL,
firstname varchar(100),
lastname varchar(100),
email varchar(100) NOT NULL,
address varchar(255),
phone varchar(100),
carid int,
primary key(customerid),
foreign key(carid) references car(carid)
);

insert into user values
(1, 'james','James','Smith', 111, 'james@carrental.com','customer'),
(2, 'michael','Michael', 'Williams', 222, 'michael@carrental.com','staff'),
(3, 'dora','Dora','Wang',333, 'dora@carrental.com','admin');

insert into car values
(1, 'ABC111', 'Toyota Prius','sliver','2021', 'rent out', 50.05),
(2, 'ABC222', 'Ford Focus','red', '2023','in garage', 68.88),
(3, 'ABC333', 'Mazda CX-60','black','2022','in garage',88.88);