from multiprocessing.sharedctypes import Value
from django.contrib.auth import get_user_model
from django.test import TestCase


class TestCustomUser(TestCase):
    
    def test_create_user(self):
        User = get_user_model()
        with self.assertRaises(TypeError):
            user = User.objects.create_user(
                email='normal@user.com',
                password='testpass'
            )