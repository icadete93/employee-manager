from django.conf.urls import url
from employees import views

urlpatterns = [
    url(r'^users/(?P<username>[A-z]+)/change-password/$', views.ChangePasswordView.as_view()),
    url(r'^$', views.UserList.as_view()),
]
