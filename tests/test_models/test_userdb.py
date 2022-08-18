from app.models.users import User, UserDB

def test_user_insert(db_test_client):
    """Tests the insert functionality of the User class by creating the UserDB, 
    initializing a User, inserting the User, and ensuring that the User in the
    UserDB is the one initialized in this test case.
    """
    
    conn, cursor = db_test_client
    userdb = UserDB(conn, cursor)

    test_user = User("test_username", "test_password")

    userdb.insert_user(test_user)

    result = userdb.select_user_by_id(1)

    assert result['username'] == "test_username"
    assert result['password'] == "test_password"

    conn.commit()


def test_user_delete(db_test_client):
    """Tests the delete functionality of the User class by creating the UserDB, 
    initializing a User, inserting the User, deleting the User, and ensuring 
    that attempting to retrieve the deleted User results in None.
    """
    
    conn, cursor = db_test_client
    userdb = UserDB(conn, cursor)
    
    test_user = User("delete_username", "delete_password")

    userdb.insert_user(test_user)

    result = userdb.select_user_by_id(2)
    assert result['username'] == "delete_username"
    assert result['password'] == "delete_password"

    userdb.delete_user_by_id(2)
    result = userdb.select_user_by_id(2)
    assert result is None 
    
    conn.commit()
