create database qlusername;
go
use qlusername;
go
create table account(
	username nvarchar(50) primary key,
	pass nvarchar(50),
);
create table classes(
	malop nvarchar(15) primary key,
);
create table student(
	mssv char(8) primary key,
	ten nvarchar(150),
	malop nvarchar(15),
	foreign key(malop) references [dbo].[classes](malop)
);
select * from student
delete from student
