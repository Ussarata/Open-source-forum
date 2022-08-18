class Comment:
    """ This is the Comment class, which is initialized with text and post_id.

    On the website, the user can add comments to a post by clicking the reply button on a post. 
    A post can exist without a comment, but a Comment cannot exist without a post. 

    Attributes: 
        text: the contents of the comment
        post_id: the post id used to identify which post the Comment belongs to 
    """

    def __init__(self, text, post_id):
        """Initializes an instance of a Comment with text and post_id."""
        self._text = text
        self._post_id = post_id

    
    @property
    def text(self):
        """Returns the text of the Comment."""
        return self._text

    
    @text.setter
    def text(self, new_text):
        """Sets the text of the Comment."""
        self._text = new_text

    
    @property
    def post_id(self):
        """Returns the post_id of the Comment."""
        return self._post_id


class CommentDB:
    """ This is the CommentDB class, which serves as the database for the Comment class. 
    This is initialized a connection and cursor to a database.

    The CommentDB is expected to be initialized using the connection and cursor to the MySQL database. 
    This can be done using the g variable, which is a special variable provided by flask to provide 
    temporary access to data globally. 

    Attributes: 
        db_conn: Connection to a database
        db_cursor: Cursor of a database
        comment: An instance of the Comment class
        comment_id: the Comment id used to identify specific comments within the database
    """

    def __init__(self, db_conn, db_cursor):
        """Initializes the CommentDB with a database connection and cursor."""
        self._db_conn = db_conn
        self._cursor = db_cursor


    def select_all_comments(self):
        """Selects all comments within the database."""
        select_all_query = """
            SELECT * from comments;
        """
        self._cursor.execute(select_all_query)

        return self._cursor.fetchall()


    def select_comments_by_post_id(self, post_id):
        """Selects comments by post_id."""
        select_comments_by_post_id = """
            SELECT * from comments WHERE post_id = %s;
        """
        self._cursor.execute(select_comments_by_post_id, (post_id,))
        return self._cursor.fetchall()

    
    def select_comment_by_id(self, comment_id):
        """Selects a Comment by the Comment id."""
        select_post_by_id = """
            SELECT * from comments WHERE comment_id = %s;
            """
        self._cursor.execute(select_post_by_id, (comment_id,))
        return self._cursor.fetchone()


    def insert_comment(self, comment):
        """Insert a Comment into the database."""
        insert_query = """
            INSERT INTO comments (text, post_id)
            VALUES (%s, %s);
            """
        
        self._cursor.execute(insert_query, (comment.text, comment.post_id))
        self._cursor.execute("SELECT LAST_INSERT_ID() comment_id")
        comment_id = self._cursor.fetchone()
        self._db_conn.commit()
        return comment_id


    def update_comment(self, comment_id, new_comment):
        """Update the text of the Comment with the corresponding comment_id value."""
        update_query = """
            UPDATE comments
            SET text = %s
            WHERE comment_id = %s;
        """

        self._cursor.execute(update_query, (new_comment.text, comment_id))
        self._db_conn.commit()


    def delete_comment_by_id(self, comment_id):
        """Delete a Comment with the corresponding comment_id value from the database."""
        delete_query = """
            DELETE from comments
            WHERE comment_id = %s;
        """

        self._cursor.execute(delete_query, (comment_id,))
        self._db_conn.commit()
