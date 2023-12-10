drop database if exists Account;
create database Account;
use Account; 
drop table if exists User;
drop table if exists File;
drop table if exists Folder;
create table User(
	role int default 2,
	id int(10) auto_increment primary key,
  email text,
  username text,
  password text
);

create table Folder(
	id INT(10) AUTO_INCREMENT PRIMARY KEY,
	path TEXT,
  name TEXT,
	date DATETIME,
	user_id INT(10),
	FOREIGN KEY(user_id) REFERENCES User(id)
);

create table File(
	id int(10) auto_increment primary key,
    path text,
    data text,
    date datetime,
    user_id int(10),
    folder_id int(10),
    foreign key(user_id) references User(id),
    foreign key(folder_id) references Folder(id)
)auto_increment = 1;

INSERT INTO user (role,id,email,username, password) VALUES
(1,1, 'admin@st.usth.edu.vn', 'admin', 'pbkdf2:sha256:600000$B26CumzGiNyLZl0g$ff5db361b37ec2b8f6b141a25aaef188ff0f7b3acf7d5b641c972821bf182a12');
