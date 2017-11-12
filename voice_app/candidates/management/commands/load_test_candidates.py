from django.core.management.base import BaseCommand, CommandError
from voice_app.accounts.api import create_mentor
from voice_app.candidates.api import create_team, create_activity, \
    create_candidate, score_activity
from datetime import datetime


class Command(BaseCommand):
    help = 'Load test data'

    def handle(self, *args, **options):

        # Create a Mentor with only 1 Team
        mentor_with_one_team = create_mentor(username='Bobby',
                                             first_name='Bob',
                                             last_name='Brown',
                                             password='bob123')
        bob_team = create_team('Team Bob', mentor_with_one_team)
        candidate1 = create_candidate('Mike', bob_team)
        mike_activity1 = create_activity(candidate1, 'Song 1',
                                         datetime(2017, 0, 1))
        mike_activity2 = create_activity(candidate1, 'Song 1',
                                         datetime(2017, 1, 1))

        candidate2 = create_candidate('Jane', bob_team)
        jane_activity1 = create_activity(candidate1, 'Song 3',
                                         datetime(2017, 0, 1))
        jane_activity2 = create_activity(candidate1, 'Song 4',
                                         datetime(2017, 1, 1))

        # Create a Mentor with 2 Teams
        mentor_with_many_teams = create_mentor(username='Loz',
                                               first_name='Laura',
                                               last_name='Mitchell',
                                               password='lozza123')
        loz_team_1 = create_team("Loz's Heroes", mentor_with_many_teams)
        loz_team_2 = create_team("Loz's Zeroes", mentor_with_many_teams)

        # Create a Mentor without a Team
        mentor_without_team = create_mentor(username='Steve-o',
                                            first_name='Steve',
                                            last_name='Clarke',
                                            password='iamlonely')

        # TODO - Create scores

        self.stdout.write(self.style.SUCCESS('Successfully loaded test data'))
