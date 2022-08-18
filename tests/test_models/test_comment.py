import pytest
from datetime import datetime

from app.models.comments import Comment
from app.models.posts import Post

def test_comment_constructor():
    """Tests the Comment constructor by ensuring that 
    the instance contains the parameters of its initialization.   
    """

    text = "Test Comment"
    post_id = "Test Post ID"

    c = Comment(text, post_id)
    assert c.text == text
    assert c.post_id == post_id

def test_comment_properties():
    """Test the properties of the Comment class by ensuring that 
    the setter functions work as intended. 
    """

    text = "Test Comment"
    post_id = "Test Post ID"

    c = Comment(text, post_id)
    assert c.text == text
    assert c.post_id == post_id

    new_text = "New Test Comment"

    c.text = new_text
    assert c.text == new_text