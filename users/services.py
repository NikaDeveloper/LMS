import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    """ Создает продукт в Stripe """
    product = stripe.Product.create(name=name)
    return product.get('id')


def create_stripe_price(product_id, amount):
    """ Создает цену в Stripe """
    price = stripe.Price.create(
        product=product_id,
        currency="rub",
        unit_amount=int(amount * 100), # Цена в копейках
    )
    return price.get('id')

def create_stripe_session(price_id):
    """ Создает сессию оплаты в Stripe """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/", # Куда вернуть юзера после оплаты
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')


def check_payment_status(session_id):
    """ Проверяет статус сессии в Stripe """
    session = stripe.checkout.Session.retrieve(session_id)
    return session.get('payment_status')
