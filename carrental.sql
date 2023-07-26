create database carrental;
use carrental;

create table catergory (
ID INT NOT NULL,
name varchar(100),
primary key(ID)
);

create table users (
userID INT NOT NULL auto_increment,
username varchar(255) NOT NULL,
firstname varchar(100),
lastname varchar(100),
password varchar(255) NOT NULL,
email varchar (100) NOT NULL,
catergoryID INT,
primary key (userID),
foreign key (catergoryID) references catergory (ID)
);

create table cars (
carID INT NOT NULL auto_increment,
numberplate varchar(100),
model varchar(255),
userID INT,
status varchar(100),
rentalfee decimal(8,2),
primary key (carID),
foreign key (userID) references users(userID)
);

insert into catergory values
(1, 'customers'),
(2, 'staff'),
(3, 'admin');

insert into users values
(1, 'JamesS','James','Smith', md5(111), 'james@carrental.com',1),
(2, 'MichaelW','Michael', 'Williams', md5(222), 'michael@carrental.com',2),
(3, 'DoraW','Dora','Wang',md5(333), 'dora@carrental.com',3);

insert into cars values
(1, 'ABC111', 'Toyota Prius', 1, 'rent out', 50.05),
(2, 'ABC222', 'Ford Focus', NUll, 'in garage', 68.88),
(3, 'ABC333', 'Mazda CX-60', NULL, 'in garage', 88.88);



