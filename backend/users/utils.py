# users/utils.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from .tokens import account_activation_token


def send_activation_email(request, user):
    """
    Sends an account activation email to the newly registered user.
    """

    # Encode user id for URL
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    # Build activation link
    domain = get_current_site(request).domain
    activation_link = f"http://{domain}/api/activate/{uidb64}/{token}/"

    # Render email template with context
    subject = "Activate Your Account - Tuzmore CRM"
    message = render_to_string("activation_email.html", {
        "user": user,
        "activation_link": activation_link,
    })

    # Send email
    email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.content_subtype = "html"  # Send as HTML
    email.send()
