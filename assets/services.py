from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def send_email(asset_name, min_value, max_value, value, created_by_id):
    user = User.objects.get(id=created_by_id)
    buy_sell_str = "compra" if value < min_value else "venda"
    lower_upper_limit = "inferior" if value < min_value else "superior"

    subject = f"Alerta de {buy_sell_str} do ativo {asset_name}!"
    message = f"Ola {user.first_name}, o ativo {asset_name} esta valendo R${value} e portanto cruzou o limite {lower_upper_limit} de R${min_value}."
    send_mail(
        subject,
        message,
        settings.DEFAULT_EMAIL_SENDER,
        [user.email],
        fail_silently=False,
    )
