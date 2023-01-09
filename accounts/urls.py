from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.register_view, name='signup-view'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('profile/', views.current_user_profile, name="current_user_profile"),
    #  URL's referentes ao reset de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html",
    ), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = "accounts/password_reset_confirm.html"
    ), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ), name='password_reset_complete'),
]
