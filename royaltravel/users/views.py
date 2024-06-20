from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic.edit import FormView
from royaltravel import settings
from .models import CustomUser
from .tokens import account_activation_token
from .forms import UserUpdateForm, RegistrationForm, ResendActivationEmailForm, ProfileUpdateForm
from django.contrib.auth import get_user_model


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    # def form_invalid(self, form):
    #     username = form.cleaned_data.get('username')
    #     User = get_user_model()
    #     try:
    #         user = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         try:
    #             user = User.objects.get(email=username)
    #         except User.DoesNotExist:
    #             user = None
    #     if user and not user.is_active:
    #         return redirect('resend_activation_email')
    #     messages.error(self.request, 'Invalid username or password')
    #     return self.render_to_response(self.get_context_data(form=form))
    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        UserModel = get_user_model()
        user = None

        if username:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                try:
                    user = UserModel.objects.get(email=username)
                except UserModel.DoesNotExist:
                    pass

        if user and not user.is_active:
            return redirect('resend_activation_email')

        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class RegistrationView(UserPassesTestMixin, FormView):
    template_name = 'users/register.html'
    form_class = RegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.last_token_generated = timezone.now()
        user.save()
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = self.request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
        message = render_to_string('users/account_activation_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        send_mail(
            'Activate your account',
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return redirect('account_activation_sent')

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(self.success_url)


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None:
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                return render(request, 'users/activation_success.html')
            else:
                messages.error(self.request, 'Verification link has been expired')
                return redirect('resend_activation_email')
        else:
            return render(request, 'users/activation_invalid.html')


class ResendActivationEmailView(FormView):
    template_name = 'users/resend_activation_email.html'
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('account_activation_sent')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        print(email)
        try:
            user = CustomUser.objects.get(email=email)
            print(user.pk, user.email)
            if not user.is_active:
                user.last_token_generated = timezone.now()
                user.save()
                token = account_activation_token.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                activation_link = self.request.build_absolute_uri(
                    reverse('activate', kwargs={'uidb64': uid, 'token': token})
                )
                message = render_to_string('users/account_activation_email.html', {'user': user,
                                                                                   'activation_link': activation_link
                                                                                   })
                send_mail('Activate your account', message, settings.EMAIL_HOST_USER, [user.email],
                          fail_silently=False)
            else:
                messages.info(self.request, 'Account is already active, you can Log in')
                return redirect('login')

        except CustomUser.DoesNotExist:
            pass
        return super().form_valid(form)


class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'users/profile.html', context)

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('profile')
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request, 'Error updating your profile')
            return render(request, 'users/profile.html', context)


def home(request):
    return render(request, 'home.html')


def about_us(request):
    return render(request, 'about_us.html')

def gallery(request):
    return render(request, 'gallery.html')

# Create your views here.
