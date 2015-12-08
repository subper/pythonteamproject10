drop table if exists member;
create table member (
	mnum integer primary key autoincrement,
	email string not null,
	pwd string not null
);