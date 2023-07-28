create database carrental;
use carrental;

create table user (
userid INT NOT NULL auto_increment,
username varchar(255) NOT NULL,
password varchar(255) NOT NULL,
email varchar (100) NOT NULL,
role varchar(60),
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
customerid INT NOT NULL auto_increment,
userid int,
firstname varchar(100),
lastname varchar(100),
address varchar(255),
phone varchar(100),
carid int,
primary key(customerid),
foreign key(carid) references car(carid),
foreign key(userid) references user(userid)
);

create table staff (
staffid INT NOT NULL auto_increment,
userid int,
firstname varchar(100),
lastname varchar(100),
phone varchar(100),
carid int,
primary key (staffid),
foreign key(carid) references car(carid),
foreign key(userid) references user(userid)
);

insert into user values
(1, 'james', '$2b$12$/RqUO/ndFG8gJ8HV3Pf39enYNFUPlq/xz8R.R/mKW2dHPbqZjqpGm', 'james@carrental.com','customer'),
(2, 'michael', '$2b$12$qWhbQbAVLU/gDq2s/sBIS.0kllMCof90.UNM6elLrvsp9Hof1UyGq', 'michael@carrental.com','staff'),
(3, 'dora','$2b$12$uEwmPw93iuZVKVlIk/vzJ.SM5rgDqWuDsXy0O2BzSThTo8i09VUxW', 'dora@carrental.com','admin');

insert into car values
(1, 'ABC111', 'Toyota Prius','sliver','2021', 'rent out', 50.05),
(2, 'ABC222', 'Ford Focus','red', '2023','in garage', 68.88),
(3, 'ABC333', 'Mazda CX-60','black','2022','in garage',88.88);



