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

SELECT * FROM [dbo].[classes]
SELECT * FROM [dbo].[student]
SELECT * FROM [dbo].account
DELETE FROM account WHERE username = 'Luc'
DELETE FROM account
DELETE FROM [classes]
DELETE FROM [student]
SET DATEFORMAT dmy;


declare @sql nvarchar(128) =
	'select *, ''k'' as [' + format(getdate(),'dd/MM/yyyy') + ']
	FROM [dbo].[students]
	WHERE [malop] = ?'
exec(@sql,'DHKHHMT12A')

select format(getdate(),'dd/MM/yyyy')

SELECT *, 'k' as (SELECT(format(getdate(),'dd/MM/yyyy')))
FROM [dbo].[students]
WHERE [malop] = 'DHKHMT12A'

SELECT *, flag = k FROM [dbo].[students] WHERE [dbo].[students].malop = 'DHKHMT12A'

insert into [dbo].[classes] values
('DHKHMT12A',7),
('DHKTPM12A',8)
insert into [dbo].[student] values
('16026501',N'Nguyễn Lê Nhật Quang','DHKHMT12A'),
('16021821',N'Võ Tấn Lực','DHKHMT12A'),
('16026801',N'Nguyễn Thành Luân','DHKHMT12A')
