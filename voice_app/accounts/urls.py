from django.conf.urls import url, include

from voice_app.accounts.views import UserLogoutView, UserLoginView


api_urlpatterns = [
    url(r'^login/$',
        UserLoginView.as_view(),
        name='api_login'),
    url(r'^logout/$',
        UserLogoutView.as_view(),
        name='api_login')
]

urlpatterns = [
    url(r'^api/', include(api_urlpatterns,
                          namespace='api_accounts')),
]
