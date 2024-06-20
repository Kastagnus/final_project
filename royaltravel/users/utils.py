from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

# ვერიფიკაციისთვს იმეილის გაგზავნა რეგისტრირებულ იუზერთან
# ვერიფიკაციის ლინკის გენერირება
def send_verification_email(user_email, token):
    subject = 'Verify Your Email Address'
    verification_link = f"{settings.SITE_URL}{reverse('verify_email')}?token={token}"
    message = f"Thank you for signing up. Please click the following link to verify your email address: {verification_link}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
