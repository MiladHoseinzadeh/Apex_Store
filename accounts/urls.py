from django.contrib.auth import views
from django.urls import path

from accounts.views import signup#, login

app_name = 'accounts'

urlpatterns = [
	path('signup/', signup, name='signup'),
	# path('login/', login, name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
]
