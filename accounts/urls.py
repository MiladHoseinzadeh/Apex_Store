from django.contrib.auth import views
from django.urls import path

from accounts.views import signup

app_name = 'accounts'

urlpatterns = [
	path('signup/', signup, name='signup'),
	path('login/', views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
]
