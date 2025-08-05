from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name="home-page"),
    path('redirect-admin', RedirectView.as_view(url="/admin/"), name="redirect-admin"),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name="login"),
    path('userlogin', views.login_user, name="login-user"),
    path('logout', views.logoutuser, name="logout"),
]

