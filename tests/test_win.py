import unittest
from app.models import Win,User

class TestWin(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Win class
    '''
    def setUp(self):
        self.user = User(username = "James",password = "potato",email = "james@ms.com")
        self.win = Win(title='Graduation',text='Today I graduated from Moringa School',user=self.user)
    
    def tearDown(self):
        Win.query.delete()
        User.query.delete()

    def test_save_win(self):
        self.win.save_win()
        self.assertTrue(len(Win.query.all())>0)