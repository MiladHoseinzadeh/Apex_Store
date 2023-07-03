from django.contrib.auth import views
from django.urls import path

from accounts.views import signup, my_account, edit_my_account

app_name = 'accounts'

urlpatterns = [
	path('signup/', signup, name='signup'),
	path('login/', views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('my_account/', my_account, name='my_account'),
	path('my_account/edit/', edit_my_account, name='edit_my_account'),
]
