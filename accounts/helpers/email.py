from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

EMAIL_TEMPLATE = """<h1>Please confirm your email for Donkey Engine account</h1>
<p>Please follow the link to verify your account:</p>
<a href="https://donkey-engine.host/confirm_email/{token}">https://donkey-engine.host/confirm_email/{token}</a>"""  # noqa: E501


def send_email_confirmation(user: User):
    token = PasswordResetTokenGenerator().make_token(user=user)
    send_mail(
        'Email confirmation',
        None,  # type: ignore
        None,
        [user.email],
        fail_silently=False,
        html_message=EMAIL_TEMPLATE.format(
            token=token,
        ),
    )
