from django.db import models

from voice_app.accounts.models import User


# Notes:
# I assumed that Teams can only have one mentor

class Team(models.Model):
    """Represents a group of Candidates who are mentored by a Mentor (User)"""
    name = models.CharField(max_length=255, null=False)
    mentor = models.ForeignKey(User, null=False)

    def average_score(self):
        candidates = self.candidate_set.all()
        if len(candidates) == 0:
            return 0
        else:
            return sum([c.average_score() for c in candidates]) / len(candidates)


# Notes:
# I decided to not use the User model for Candidates since the requirements
# did not need the candidates to have login functionality.

class Candidate(models.Model):
    """A participant on The Voice"""

    name = models.CharField(max_length=255, null=False)
    team = models.ForeignKey(Team, null=False)

    def average_score(self):
        activities = self.activity_set.all()
        if len(activities) == 0:
            return 0
        else:
            return sum([a.average_score() for a in activities]) / len(activities)


class Activity(models.Model):
    """A performance by a participant"""

    candidate = models.ForeignKey(Candidate, null=False)
    song_name = models.CharField(max_length=255, null=False)
    performance_date = models.DateField(null=False)

    def average_score(self):
        scores = self.activityscore_set.all()
        if len(scores) == 0:
            return 0
        else:
            return sum([score.score for score in scores]) / len(scores)


class ActivityScore(models.Model):
    """A score given by a Mentor on an Activity"""

    class Meta:
        unique_together = (
            ('activity', 'mentor'),
        )

    activity = models.ForeignKey(Activity, null=False)
    mentor = models.ForeignKey(User, null=False)
    score = models.PositiveIntegerField(null=False)
