drop database if exists Account;
create database Account;
use Account;
drop table if exists user;

create table user(
    role int default 2,
    id int(10) auto_increment primary key,
    email text,
    username text,
    password text,
    UNIQUE KEY (username(255))
);

drop table if exists folder;
create table folder(
    id int(10) auto_increment primary key,
    path text,
    name text,
    date datetime,
    user_id int(10),
    parent_folder_id int(10),
    foreign key(user_id) references user(id)
);

drop table if exists file;
create table file(
    id int(10) auto_increment primary key,
    path text,
    name text,
    date datetime,
    user_id int(10),
    folder_id int(10),
    foreign key(user_id) references user(id),
    foreign key(folder_id) references folder(id)
);

INSERT INTO user (role,id,email,username, password) VALUES
(1,1, 'admin@st.usth.edu.vn', 'admin', 'pbkdf2:sha256:600000$B26CumzGiNyLZl0g$ff5db361b37ec2b8f6b141a25aaef188ff0f7b3acf7d5b641c972821bf182a12');

