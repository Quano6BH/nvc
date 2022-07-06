CREATE TABLE Discord (
    email varchar(255),
    password varchar(255),
    two_fa varchar(255),
    token varchar(255),
    profile_name varchar(255),
    status varchar(255),
    date_created DATETIME,
    date_modified DATETIME
);

CREATE TABLE Twitter (
    username varchar(255),
    password varchar(255),
    two_fa varchar(255),
    recovery_email varchar(255),
    recovery_password varchar(255),
    status varchar(255),
    profile_id varchar(255),
    date_created DATETIME,
    date_modified DATETIME
);