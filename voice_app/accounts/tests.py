from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from voice_app.accounts.api import create_mentor
from voice_app.accounts.models import User


class APITestCase(TestCase):

    def test_create_mentor(self):
        mentor = create_mentor('TestMentor', 'Test',
                               'Mentor', 'password')

        mentor_id = mentor.id

        retrieved_mentor = User.objects.get(pk=mentor_id)

        self.assertEqual(mentor.username,
                         retrieved_mentor.username)

        self.assertEqual(mentor.first_name,
                         retrieved_mentor.first_name)

        self.assertEqual(mentor.last_name,
                         retrieved_mentor.last_name)

        self.assertEqual(mentor.is_mentor, True)

        self.assertEqual(mentor.fullname,
                         'Test Mentor')

    def test_duplicate_mentor_creation(self):

        create_mentor('TestMentor', 'Test',
                      'Mentor', 'password')

        with self.assertRaises(IntegrityError) as e:
            create_mentor('TestMentor', 'Test',
                          'Mentor', 'password')


class UserLoginViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:api_accounts:api_login')

    def test_url(self):
        self.assertEqual('/accounts/api/login/', self.url)

    def test_bad_input(self):

        # Test no password sent
        response = self.client.post(self.url, {
            'username': 'Test'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, ['NO_PASSWORD'])

        # Test no username sent
        response = self.client.post(self.url, {
            'password': 'password'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, ['NO_USERNAME'])

        # Test no user with cred
        response = self.client.post(self.url, {
            'username': 'Test',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, ['INVALID_CREDENTIALS'])

    def test_login_works(self):
        create_mentor('Mentor', 'Men', 'Tor', 'password')
        response = self.client.post(self.url, {
            'username': 'Mentor',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 201)


class UserLogoutViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:api_accounts:api_logout')

    def test_url(self):
        self.assertEqual('/accounts/api/logout/', self.url)

    def test_logout_without_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_logout_works(self):
        create_mentor('Mentor', 'Men', 'Tor', 'password')
        r = self.client.post(
            reverse('accounts:api_accounts:api_login'),
            {
                'username': 'Mentor',
                'password': 'password'
            })
        self.assertEqual(r.status_code, 201)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ProfileViewTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:api_accounts:api_profile')

    def test_url(self):
        self.assertEqual('/accounts/api/profile/', self.url)

    def test_profile_works(self):
        mentor = create_mentor('Mentor', 'Men', 'Tor', 'password')
        self.client.post(
            reverse('accounts:api_accounts:api_login'),
            {
                'username': 'Mentor',
                'password': 'password'
            }
        )
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data,
                             {
                                 'id': mentor.id,
                                 'username': mentor.username,
                                 'first_name': mentor.first_name,
                                 'last_name': mentor.last_name,
                                 'is_admin': mentor.is_superuser,
                                 'is_mentor': mentor.is_mentor
                             })
