from django.db import IntegrityError
from django.test import TestCase

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

    def test_duplicate_mentor_creation(self):

        create_mentor('TestMentor', 'Test',
                      'Mentor', 'password')

        with self.assertRaises(IntegrityError) as e:
            create_mentor('TestMentor', 'Test',
                          'Mentor', 'password')
