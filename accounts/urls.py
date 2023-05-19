from django.urls import path

from accounts.views import signup

app_name = 'accounts'

urlpatterns = [
	path('signup/', signup, name='signup'),
]
