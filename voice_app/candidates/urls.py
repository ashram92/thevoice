from django.conf.urls import url, include

from voice_app.candidates.views import TeamsView

api_urlpatterns = [
    url(r'^teams/$',
        TeamsView.as_view(),
        name='api_teams'),
]

urlpatterns = [
    url(r'^api/', include(api_urlpatterns,
                          namespace='api_candidates')),
]
