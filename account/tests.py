from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()


class CustomUserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username = 'testname',
            email = 'testname@email.com',
            password = 'c0rrecth0rse',
        )
        self.assertEqual(user.username, 'testname')
        self.assertEqual(user.email, 'testname@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username = 'testsuperuser',
            email = 'testsuperuser@email.com',
            password = 'c0rrecth0rse',
        )
        self.assertEqual(admin_user.username, 'testsuperuser')
        self.assertEqual(admin_user.email, 'testsuperuser@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
