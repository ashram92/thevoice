from django.conf.urls import url, include

from voice_app.accounts.views import UserLogoutView, UserLoginView, ProfileView

api_urlpatterns = [
    url(r'^login/$',
        UserLoginView.as_view(),
        name='api_login'),
    url(r'^logout/$',
        UserLogoutView.as_view(),
        name='api_logout'),
    url(r'^profile/$',
        ProfileView.as_view(),
        name='api_profile')
]

urlpatterns = [
    url(r'^api/', include(api_urlpatterns,
                          namespace='api_accounts')),
]
