from voice_app.accounts.models import User
from voice_app.candidates.models import Team, Candidate, Activity, \
    ActivityScore

MIN_SCORE = 0
MAX_SCORE = 100


def create_team(team_name: str, mentor: User):

    team = Team(name=team_name, mentor=mentor)
    team.save(force_insert=True)
    return team


def create_candidate(name: str, team: Team):
    candidate = Candidate(name=name,
                          team=team)
    candidate.save(force_insert=True)
    return candidate


def create_activity(candidate, song_name, performance_date):
    activity = Activity(candidate=candidate,
                        song_name=song_name,
                        performance_date=performance_date)
    activity.save()
    return activity


def score_activity(activity, mentor, score):
    if MIN_SCORE <= score <= MAX_SCORE:

        score = ActivityScore(activity=activity,
                              mentor=mentor,
                              score=score)
        score.save()
        return score
    else:
        raise ValueError('Score `{}` is out of range. '
                         'Min: {} | Max: {}'.format(score, MIN_SCORE,
                                                    MAX_SCORE))

