class User:
    """ This is the User class, which is initialized with username and password.

    The User class has a composition relationship with the Post class.
    If an instance of a User class with a Post is deleted, the Post associated with
    the User is also deleted. 
    On the website, the User can be created by clicking the Register button and inputting a Username and Password. 
    The id of the User class is also used in the Post class and Comment class as a foreign key.

    Attributes: 
        username: The username of the User
        password: The password of the User 
    """
    def __init__(self, username, password):
        """ Initializes an instance of a User with username and password."""
        self._username = username
        self._password = password

    
    @property
    def username(self):
        """Returns the username of the User."""
        return self._username


    @username.setter
    def username(self, new_username):
        """Sets the username of the User."""
        self._username = new_username


    @property
    def password(self):
        """Returns the password of the User."""
        return self._password


class UserDB:
    """ This is the UserDB class, which serves as the database for the User class. 
    This is initialized a connection and cursor to a database.

    The UserDB is expected to be initialized using the connection and cursor to the MySQL database. 
    This can be done using the g variable, which is a special variable provided by flask to provide 
    temporary access to data globally. 

    Attributes: 
        db_conn: Connection to a database
        db_cursor: Cursor of a database
        user: An instance of the User class
        user_id: the User ID used to identify specific users within the database
    """

    def __init__(self, db_conn, db_cursor):
        """Initializes the UserDB with a database connection and cursor."""
        self._db_conn = db_conn
        self._cursor = db_cursor


    def select_all_users(self):
        """Selects all users within the database."""
        select_all_query = """
            SELECT * from users;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()

    
    def select_user_by_username(self, username):
        """Selects a User by username."""
        select_user_by_username = """
            SELECT * from users WHERE username = %s;
        """
        self._cursor.execute(select_user_by_username, (username,))
        return self._cursor.fetchone()

    
    def select_user_by_password(self, password):
        """Selects a User by password."""
        select_user_by_password = """
            SELECT * from users WHERE username = %s;
        """
        self._cursor.execute(select_user_by_password, (password,))
        return self._cursor.fetchone()

    
    def select_user_by_id(self, user_id):
        """Selects a User by user_id."""
        select_user_by_id = """
            SELECT * from users WHERE user_id = %s;
            """
        self._cursor.execute(select_user_by_id, (user_id,))
        return self._cursor.fetchone()


    def insert_user(self, user):
        """Insert a User into the database."""
        insert_query = """
            INSERT INTO users (username, password)
            VALUES (%s, %s);
            """
        
        self._cursor.execute(insert_query, (user.username, user.password))
        self._cursor.execute("SELECT LAST_INSERT_ID() user_id")
        user_id = self._cursor.fetchone()
        self._db_conn.commit()
        return user_id


    def update_user(self, user_id, new_user):
        """Update the username of the User with the corresponding user_id value."""
        update_query = """
            UPDATE users
            SET username = %s
            WHERE user_id = %s;
        """

        self._cursor.execute(update_query, (new_user.username, user_id))
        self._db_conn.commit()


    def delete_user_by_id(self, user_id):
        """Delete a User with the corresponding user_id value from the database."""
        delete_query = """
            DELETE from users
            WHERE user_id = %s;
        """

        self._cursor.execute(delete_query, (user_id,))
        self._db_conn.commit()
