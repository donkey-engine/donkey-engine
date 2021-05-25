from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

EMAIL_TEMPLATE = """<h1>Пожалуйста, подтвердите свой email для учетной записи Donkey Engine</h1>
<p>Пожалуйста, перейдите по ссылке, чтобы подтвердить свою учетную запись:</p>
<a href="http://0.0.0.0:8002/api/confirm_email/?token={token}&username={username}">
http://0.0.0.0:8002/api/confirm_email/?token={token}&username={username}
</a>"""  # noqa: E501


def send_email_confirmation(user: User):
    if settings.EMAIL_ENABLED:
        token = PasswordResetTokenGenerator().make_token(user=user)
        send_mail(
            'Email confirmation',
            None,  # type: ignore
            None,
            [user.email],
            fail_silently=False,
            html_message=EMAIL_TEMPLATE.format(
                token=token, username=user.username,
            ),
        )
