from django.conf.urls import url
from django.contrib.auth.views import LoginView
from . import views

app_name = "users"
urlpatterns = [
    url(r"login/$",LoginView.as_view(template_name='users/login.htm'),
        name="login"),
    url(r"logout/$",views.logout_view,name="logout"),
    url(r"register/$",views.register,name="register"),
]
