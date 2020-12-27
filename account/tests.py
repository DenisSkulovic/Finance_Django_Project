from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from account.forms import CustomUserCreationForm
from account.views import SignUpView
User = get_user_model()

# setUpTestData can be used to speed up testing, if it's too slow


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

class SignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'signup.html')
        # self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'SOME TEXT THAT SHOULD NOT BE HERE')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__,
            SignUpView.as_view().__name__,
        )