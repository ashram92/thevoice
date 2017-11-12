from datetime import datetime
from random import randint

from django.core.management.base import BaseCommand

from voice_app.accounts.api import create_mentor
from voice_app.candidates.api import create_team, create_activity, \
    create_candidate, score_activity, MIN_SCORE, MAX_SCORE


class Command(BaseCommand):
    help = 'Load test data into the database. Mostly randomised :D'

    def __init__(self):
        super().__init__()
        self.mentors = []
        self.activities = []

    def score_activities(self):
        for activity in self.activities:
            for mentor in self.mentors:
                if randint(1, 5) != 5:  # Do not score 20% of the time
                    score_activity(activity, mentor,
                                   randint(MIN_SCORE, MAX_SCORE))

    def create_activities_for_candidate(self, candidate, number_of_activities):
        if number_of_activities > 10:
            number_of_activities = 10  # Let's limit it to 10

        for i in range(1, number_of_activities + 1):
            self.activities.append(
                create_activity(candidate,
                                "{}'s Song {}".format(candidate.name, i),
                                datetime(2017, i, 1))
            )

    def handle(self, *args, **options):

        # Create a Mentor with only 1 Team
        bob = create_mentor(username='Bob',
                            first_name='Bob',
                            last_name='Brown',
                            password='bobbrown')
        bob_team = create_team('Team Bob', bob)
        mike = create_candidate('Mike', bob_team)
        self.create_activities_for_candidate(mike, 5)
        jane = create_candidate('Jane', bob_team)
        self.create_activities_for_candidate(jane, 3)
        doug = create_candidate('Doug', bob_team)
        self.create_activities_for_candidate(doug, 3)

        # Create a Mentor with 2 Teams
        laura = create_mentor(username='Laura',
                              first_name='Laura',
                              last_name='Mitchell',
                              password='lauramitchell')
        laura_team_1 = create_team("Loz's Heroes", laura)
        oliver = create_candidate('Oliver', laura_team_1)
        self.create_activities_for_candidate(oliver, 10)
        robin = create_candidate('Robin', laura_team_1)
        self.create_activities_for_candidate(robin, 1)

        laura_team_2 = create_team("Loz's Zeroes", laura)
        jack = create_candidate('Jack', laura_team_2)
        self.create_activities_for_candidate(jack, 8)

        # Create a Mentor without a Team
        steve = create_mentor(username='Steve',
                              first_name='Steve',
                              last_name='Clarke',
                              password='steveclarke')

        self.mentors = [bob, laura, steve]
        self.score_activities()

        self.stdout.write(self.style.SUCCESS('Successfully loaded test data'))
