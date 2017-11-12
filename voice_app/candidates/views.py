# Create your views here.
from rest_framework import permissions, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from voice_app.candidates.models import Team, Candidate, Activity


class ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = (
            'song_name',
            'performance_date',
            'average_score',
        )


class CandidateSerializer(serializers.ModelSerializer):

    activities = ActivitySerializer(many=True, source='activity_set')

    class Meta:
        model = Candidate
        fields = (
            'id',
            'name',
            'activities',
            'average_score',
        )


class TeamSerializer(serializers.ModelSerializer):

    candidates = CandidateSerializer(many=True, source='candidate_set')

    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'mentor',
            'candidates',
            'average_score',
        )


class TeamsView(ListAPIView):
    """Retrieve all team data relative to current logged in user.
        - Admin: Can retrieve all data
        - Mentor: Can retireve the teams he mentors
    """
    serializer_class = TeamSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Team.objects.select_related('mentor').prefetch_related(
                    'candidate_set',
                    'candidate_set__activity_set',
                    'candidate_set__activity_set__activityscore_set')

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_mentor:
            q = self.get_queryset().filter(mentor_id=user.id)
        elif user.is_superuser:
            q = self.get_queryset()
        else:
            raise PermissionDenied('You do not have access to teams.')

        serializer = self.serializer_class(list(q.all()), many=True)
        return Response(serializer.data)
