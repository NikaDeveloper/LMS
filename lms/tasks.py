from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """ Асинхронная задача для отправки писем об обновлении курса """
    try:
        course = Course.objects.get(pk=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        recipient_list = [sub.user.email for sub in subscriptions if sub.user.email]

        if recipient_list:
            send_mail(
                subject=f'Обновление курса: {course.title}',
                message=f'Курс "{course.title}" был обновлен. Зайдите посмотреть новые материалы!',
                from_email=settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@lms.com',
                recipient_list=recipient_list,
                fail_silently=False
            )
            print(f"Письма отправлены подписчикам курса {course.title}")

    except Course.DoesNotExist:
        print(f"Курс с id {course_id} не найден.")
