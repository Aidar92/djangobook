from myshop.celery import app
from django.core.mail import send_mail
from .models import Order

@app.task
def order_created(order_id):
    """
    Task to send and e-mail notification when an order is successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'
    message = f'Dear {order.first_name}, \n\nYou have successfully placed an order.\
        Your order id is {order.id}'
    mail_sent = send_mail(subject, message, 'aydargumerov@gmail.com', [order.email])
    return mail_sent