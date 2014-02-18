from django.core.urlresolvers import reverse
from django_webtest import WebTest
from tests.factories import UserFactory


class HomeTests(WebTest):
    def test_home_not_authenticated(self):
        url = reverse('home')
        response = self.app.get(url)
        self.assertContains(response, 'Welcome!')
        self.assertContains(response, 'Please login to see your notes')

    def test_home_authenticated(self):
        url = reverse('home')
        user = UserFactory()
        response = self.app.get(url, user=user)
        self.assertContains(response, 'Welcome!')
        self.assertContains(response, 'Have a look at your notes')
