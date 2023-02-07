from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from orders.models import Order
from robots.models import Robot


@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
	'''
	Этот приемник срабатывает, когда генерируется сигнал post_save для модели Order, 
	После того, как модель Order была сохранена в базе данных, модель Order генерирует 
	сигнал post_save, проверять есть ли в базе данных нужный нам робот и отправляет 
	соответствующие ответы заказчикам.
	'''
	if created:
		robots = Robot.objects.all()
		for robot in robots:
			if robot.serial == instance.robot_serial:
				message_one = f'Спасибо за заказ. Робот модели {robot.model}, версии {robot.version} есть в наличии. Ожидайте. Наш оператор свяжется с вами.'
				send_mail('Информация о вашем заказе в R4C.', message_one,'r4c@info.com', [instance.customer], fail_silently=False)
				break
			else:
				message_two = 'Робот который интересует вас нет в наличии. Как только он появится в наличии мы с вами свяжемся.'
				send_mail('Информация о вашем заказе в R4C.', message_two, 'r4c@info.com', [instance.customer], fail_silently=False) 
				break


@receiver(post_save, sender=Robot)
def create_robot(sender, instance, created, **kwargs):
	'''
	Этот приемник срабатывает, когда генерируется сигнал post_save для модели Robot, 
	После того, как модель Robot была сохранена в базе данных, модель Robot генерирует 
	сигнал post_save, проверять есть ли в базе данных нужный нам заказ и отправляет 
	соответствующие ответы заказчикам.
	'''
	if created:
		orders = Order.objects.all()
		for order in orders:
			if order.robot_serial == instance.serial:
				message_three = f'Добрый день! Недавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}. Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.'
				send_mail('Информация о вашем заказе в R4C.', message_three, 'r4c@info.com', [order.customer], fail_silently=False)
				break

