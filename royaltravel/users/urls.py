from django.views.generic import RedirectView, TemplateView

from .views import RegistrationView, MyLoginView, ActivateAccountView, ResendActivationEmailView, MyProfile
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('login/', MyLoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html',
                                                      html_email_template_name='users/password_reset_email.html'),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('account_activation_sent/', TemplateView.as_view(template_name='users/account_activation_sent.html'),
         name='account_activation_sent'),
    path('resend_activation_email', ResendActivationEmailView.as_view(), name='resend_activation_email'),
    path('profile/', MyProfile.as_view(), name='profile'),
    path('about/', views.about_us, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('', views.home, name='home')
]