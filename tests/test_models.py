import unittest
from app.models import User,Blog

class UserTest(unittest.TestCase):

    def setUp(self):
       self.new_user = User(username = 'erastus',email='erastuskariuki15@gmail.com',bio='Tech-specialist',password='@e1r2a3s4#')
    
    def test_password_setter(self):
       self.assertTrue(self.new_user.pass_secure is not None)
    
    def test_no_password_access(self):
       self.assertTrue(AttributeError):
       self.new_user.pass_secure
    
    def test_password_verification(self):
       self.assertTrue(self.new_user.verify_password('333'))