from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from mainpage.views import MainpageTemplateView



class MainpageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('mainpage')
        self.response = self.client.get(url)

    def test_mainpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_mainpage_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_mainpage_template(self):
        self.assertTemplateUsed(self.response, 'mainpage.html')

    # def test_mainpage_contains_correct_html(self):
    #     self.assertContains(self.response, 'TEMPORARY MAINPAGE TEXT') ###############

    def test_mainpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, 'SOME TEXT THAT SHOULD NOT BE THERE') #############

    def test_mainpage_url_resolves_mainpageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            MainpageTemplateView.as_view().__name__,
        )