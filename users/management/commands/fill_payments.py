from django.core.management.base import BaseCommand
from users.models import Payment, User
from lms.models import Course, Lesson

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми платежами'

    def handle(self, *args, **options):
        user = User.objects.first()
        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR('Сначала создайте хотя бы одного пользователя!'))
            return

        payment_list = [
            {
                "user": user,
                "payment_date": "2023-10-20",
                "course": course,
                "lesson": None,
                "amount": 15000.00,
                "payment_method": "transfer"
            },
            {
                "user": user,
                "payment_date": "2023-10-25",
                "course": None,
                "lesson": lesson,
                "amount": 1000.50,
                "payment_method": "cash"
            },
        ]

        for payment_data in payment_list:
            payment, created = Payment.objects.get_or_create(
                user=payment_data["user"],
                course=payment_data["course"],
                lesson=payment_data["lesson"],
                defaults={
                    "payment_date": payment_data["payment_date"],
                    "amount": payment_data["amount"],
                    "payment_method": payment_data["payment_method"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Платеж создан: {payment}'))
            else:
                self.stdout.write(self.style.WARNING(f'Платеж уже существует: {payment}'))
