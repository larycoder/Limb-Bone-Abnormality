drop database if exists Account;
create database Account;
use Account;
drop table if exists User;
drop table if exists Folder;
drop table if exists File;
create table User(
    role int default 2,
    id int(10) auto_increment primary key,
    email text,
    username text,
    password text,
    UNIQUE KEY (username(255))
);
create table Folder(
    id int(10) auto_increment primary key,
    path text,
    name text,
    date datetime,
    user_id int(10),
    parent_folder_id int(10),
    foreign key(user_id) references User(id)
);
create table File(
    id int(10) auto_increment primary key,
    path text,
    name text,
    date datetime,
    user_id int(10),
    folder_id int(10),
    foreign key(user_id) references User(id),
    foreign key(folder_id) references Folder(id)
);

INSERT INTO User (role,id,email,username, password) VALUES
(1,1, 'admin@st.usth.edu.vn', 'admin', 'pbkdf2:sha256:600000$B26CumzGiNyLZl0g$ff5db361b37ec2b8f6b141a25aaef188ff0f7b3acf7d5b641c972821bf182a12');

