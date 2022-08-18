class Post:
    """ This is the Post class, which is initialized with title, content, and user_id. 

    The Post class has a composition relationship with the Comment class.
    If an instance of a Post class with a Comment is deleted, the Comment associated with 
    the Post class is also deleted. 
    On the website, the user can create a post by clicking the Post button and inputting the Username, title of the post,
    and the content. 
    A user can exist without a post, but a post cannot exist without the user. 

    Attributes: 
        title: The title of the post
        content: The content of the post
        user_id: The id of the user creating the post
    """
    def __init__(self, title, content, user_id):
        """Initializes an instance of a Post with title, content, and user_id."""
        self._title = title
        self._content = content
        self._user_id = user_id

    
    @property
    def title(self):
        """Returns the title of the Post."""
        return self._title

    
    @title.setter
    def title(self, new_title):
        """Sets the title of the Post."""
        self._title = new_title

    
    @property
    def content(self):
        """Returns the content of the Post."""
        return self._content


    @content.setter
    def content(self, new_content):
        """Sets the content of the Post."""
        self._content = new_content


    @property
    def user_id(self):
        """Returns the user_id of the Post."""
        return self._user_id


class PostDB:
    """ This is the PostDB class, which serves as the database for the Post class. 
    This is initialized a connection and cursor to a database.

    The PostDB is expected to be initialized using the connection and cursor to the MySQL database. 
    This can be done using the g variable, which is a special variable provided by flask to provide 
    temporary access to data globally. 

    Attributes: 
        db_conn: Connection to a database
        db_cursor: Cursor of a database
        post: An instance of the Post class
        post_id: the Post ID used to identify specific Posts within the database
    """
    def __init__(self, db_conn, db_cursor):
        """Initializes the PostDB with a database connection and cursor."""
        self._db_conn = db_conn
        self._cursor = db_cursor


    def select_all_posts(self):
        """Selects all Posts within the database."""
        select_all_query = """
            SELECT * from posts;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()

    
    def select_posts_by_user_id(self, user_id):
        """Selects Posts using user_id."""
        select_posts_by_user_id = """
            SELECT * from posts WHERE user_id = %s;
        """
        self._cursor.execute(select_posts_by_user_id, (user_id,))
        return self._cursor.fetchall()

    
    def select_post_by_title(self, title):
        """Selects Posts using title."""
        select_post_by_title = """
            SELECT * from posts WHERE title = %s;
        """
        self._cursor.execute(select_post_by_title, (title,))
        return self._cursor.fetchone()

    
    def select_post_by_id(self, post_id):
        """Selects Posts using post_id."""
        select_post_by_id = """
            SELECT * from posts WHERE post_id = %s;
            """
        self._cursor.execute(select_post_by_id, (post_id,))
        return self._cursor.fetchone()


    def insert_post(self, post):
        """Insert a Post into the database."""
        insert_query = """
            INSERT INTO posts (title, content, user_id)
            VALUES (%s, %s, %s);
            """
        
        self._cursor.execute(insert_query, (post.title, post.content, post.user_id))
        self._cursor.execute("SELECT LAST_INSERT_ID() post_id")
        post_id = self._cursor.fetchone()
        self._db_conn.commit()
        return post_id


    def update_post(self, post_id, new_post):
        """Update the title and content of the Post with the corresponding post_id value"""
        update_query = """
            UPDATE posts
            SET content = %s
            WHERE post_id = %s;
        """

        self._cursor.execute(update_query, (new_post.content, post_id))
        self._db_conn.commit()


    def delete_post_by_id(self, post_id):
        """Delete a Post with the corresponding post_id value from the database"""
        delete_query = """
            DELETE from posts
            WHERE post_id = %s;
        """

        self._cursor.execute(delete_query, (post_id,))
        self._db_conn.commit()
