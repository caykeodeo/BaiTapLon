create database qlusername;
go
use qlusername;
go
create table account(
	username nvarchar(50) primary key,
	pass nvarchar(50),
);
create table student(
	mssv nvarchar(50) primary key,
	ten nvarchar(50),
	lop nvarchar(50)
);
select * from account
select * from student

drop table account
drop table student