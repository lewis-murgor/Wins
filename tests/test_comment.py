import unittest
from app.models import Comment,Win,User

class TestComment(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Comment class
    '''
    def setUp(self):
        self.new_user = User(username = "Lewis",password = "king",email = "lewis@gmail.com")
        self.new_win = Win(title='Graduation',text='Today I graduated from Moringa School',user=self.new_user)
        self.comment = Comment(comment='congratulations',win = self.new_win,user = self.new_user)

    def tearDown(self):
        Comment.query.delete()
        Win.query.delete()
        User.query.delete()

    def test_save_comment(self):
        self.comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)