"""
Collection of functions to help establish the database
"""
import mysql.connector


# Connect to MySQL and the task database
def connect_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"],
        database=config["DATABASE"]
    )
    return conn


# Setup for the Database
#   Will erase the database if it exists
def init_db(config):
    conn = mysql.connector.connect(
        host=config["DBHOST"],
        user=config["DBUSERNAME"],
        password=config["DBPASSWORD"]
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"DROP DATABASE IF EXISTS {config['DATABASE']};")
    cursor.execute(f"CREATE DATABASE {config['DATABASE']};")
    cursor.execute(f"use {config['DATABASE']};")
    cursor.execute(
        f""" 
        CREATE TABLE tasks
        (
            id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            description VARCHAR(50),
            creation_datetime timestamp,
            completed TINYINT(1),
            CONSTRAINT pk_todo PRIMARY KEY (id)
        );
        """
    )

    cursor.execute(
        f"""
        CREATE TABLE users
        (
            user_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            username VARCHAR(20) NOT NULL,
            password VARCHAR(30) NOT NULL,
            CONSTRAINT pk_user PRIMARY KEY (user_id),
            CONSTRAINT unique_username UNIQUE (username)
        );
        """
    )

    cursor.execute(
        f"""
        CREATE TABLE posts
        (
            post_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            user_id SMALLINT UNSIGNED NOT NULL,
            title VARCHAR(50) NOT NULL,
            content VARCHAR(500) NOT NULL,
            CONSTRAINT pk_post PRIMARY KEY (post_id),
            CONSTRAINT fk_user FOREIGN KEY (user_id) 
                REFERENCES users (user_id)
            ON DELETE RESTRICT ON UPDATE CASCADE,
            CONSTRAINT unique_title UNIQUE (title)
        );
        """
    )

    cursor.execute(
        f"""
        CREATE TABLE comments
        (
            comment_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
            post_id SMALLINT UNSIGNED NOT NULL,
            text VARCHAR(300) NOT NULL,
            CONSTRAINT pk_comment PRIMARY KEY (comment_id),
            CONSTRAINT fk_post FOREIGN KEY (post_id) 
                REFERENCES posts (post_id)
            ON DELETE RESTRICT ON UPDATE CASCADE
        );
        """
    )

    cursor.close()
    conn.close()
