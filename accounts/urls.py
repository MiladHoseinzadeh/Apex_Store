from django.urls import path

from accounts.views import signup#, login_old

app_name = 'accounts'

urlpatterns = [
	path('signup/', signup, name='signup'),
	# path('login/', login_old, name='login'),
]
