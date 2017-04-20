from django.conf.urls import url
from employees import views

urlpatterns = [
    url(r'^users/(?P<username>[A-z]+)/change-password/$', views.ChangePasswordView.as_view()),
    url(r'^$', views.UserList.as_view()),
    url(r'^reset_password/$', views.ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.PasswordResetConfirmView.as_view(), name="reset_password_confirm"),

]
