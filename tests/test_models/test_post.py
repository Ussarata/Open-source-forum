import pytest
from datetime import datetime

from app.models.posts import Post 

def test_post_constructor():
    """Tests the Post constructor by ensuring that 
    the instance contains the parameters of its initialization.   
    """
    title = "Test Title"
    content = "Test Content"
    user_id = 1
    p = Post(title, content, user_id)
    assert p.title == title
    assert p.content == content
    assert p.user_id == user_id 

def test_post_properties():
    """Test the properties of the Post class by ensuring that 
    the setter functions work as intended. 
    """

    title = "Property Test Title"
    content = "Property Test Content"
    user_id = 1

    p = Post(title, content, user_id)
    assert p.title == title
    assert p.content == content
    
    new_title = "New Property Test Title"
    new_content = "New Property Test Content"

    p.title = new_title
    p.content = new_content

    assert p.title == new_title    
    assert p.content == new_content
