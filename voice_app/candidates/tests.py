from datetime import datetime

from django.test import TestCase

# Create your tests here.
from voice_app.accounts.api import create_mentor
from voice_app.candidates.api import create_team, create_candidate, \
    create_activity, score_activity


class CandidateAPITestCase(TestCase):

    def setUp(self):
        self.mentor = create_mentor('Mentor',
                                    'Men',
                                    'Tor',
                                    'password')

    def _create_team(self):
        return create_team('Mentor Team', self.mentor)

    def _create_candidate(self, team):
        return create_candidate('Candidate Bob', team)

    def _create_activity(self, candidate, date):
        return create_activity(candidate, 'Song 1', date)

    def test_create_team(self):
        team = self._create_team()
        self.assertEqual(team.name, 'Mentor Team')

    def test_create_candidate(self):
        team = self._create_team()
        candidate = self._create_candidate(team)
        self.assertEqual(candidate.name, 'Candidate Bob')
        self.assertEqual(candidate.team.id, team.id)

    def test_create_activity(self):
        candidate = self._create_candidate(self._create_team())
        activity = self._create_activity(candidate, datetime(2017, 1, 1))
        self.assertEqual(activity.candidate, candidate)
        self.assertEqual(activity.song_name, 'Song 1')
        self.assertEqual(activity.performance_date, datetime(2017, 1, 1))

    def test_create_activity_score(self):
        team = self._create_team()
        candidate = self._create_candidate(team)
        activity = self._create_activity(candidate, datetime(2017, 1, 1))

        with self.assertRaises(ValueError):
            score_activity(activity, self.mentor, -1)

        with self.assertRaises(ValueError):
            score_activity(activity, self.mentor, 101)

        score = score_activity(activity, self.mentor, 50)
        self.assertEqual(score.score, 50.0)
