from django.urls import path
from .views import SignUp, login_page,  logout_page, profile_page

app_name="users"
urlpatterns = [
    path("register/", SignUp.as_view(), name="register"),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("profile/", profile_page, name="profile"),  
]