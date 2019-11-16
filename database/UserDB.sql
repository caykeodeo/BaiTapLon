create database qlusername;
go
use qlusername;
go
create table account(
	username nvarchar(50) primary key,
	pass nvarchar(50),
);
select * from account
delete from account