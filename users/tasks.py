from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User


@shared_task
def block_inactive_users():
    """ Блокирует пользователей, которые не заходили больше месяца """
    # Вычисляем дату
    one_month_ago = timezone.now() - timedelta(days=30)
    # Находим активных пользователей, у которых last_login старее месяца
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
        is_staff=False,
        is_superuser=False
    )

    count = inactive_users.count()
    if count > 0:
        # Массовое обновление (быстрее, чем цикл)
        inactive_users.update(is_active=False)
        print(f"Заблокировано {count} пользователей за неактивность.")
    else:
        print("Неактивных пользователей для блокировки не найдено.")
