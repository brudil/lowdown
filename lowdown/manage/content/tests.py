from django.contrib.auth import get_user_model
from django.test import TestCase


class ListContentViewTestCase(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_superuser(username='test', email='test@test.test', password='test')

    def test_index(self):
        self.client.login(username='test', password='test')
        resp = self.client.get('/manage/content/')
        self.assertEqual(resp.status_code, 200)
