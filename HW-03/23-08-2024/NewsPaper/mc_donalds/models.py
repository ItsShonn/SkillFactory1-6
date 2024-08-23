from django.db import models
from datetime import datetime
from datetime import timezone


class Product(models.Model):
	name = models.CharField(max_length=255)
	price = models.FloatField(default=0.0)
	composition = models.TextField(default="Состав не указан")


class Staff(models.Model):
	director = 'DI'
	admin = 'AD'
	cook = 'CO'
	cashier = 'CA'
	cleaner = 'CL'

	POSITIONS = [
		(director, 'Директор'),
		(admin, 'Администратор'),
		(cook, 'Повар'),
		(cashier, 'Кассир'),
		(cleaner, 'Уборщик')
	]

	full_name = models.CharField(max_length=255)
	position = models.CharField(max_length=2,
								choices=POSITIONS,
								default=cashier)
	labor_contract = models.IntegerField()

	def get_last_name(self):
		return self.full_name.split()[0]


class Order(models.Model):
	time_in = models.DateTimeField(auto_now_add=True)
	time_out = models.DateTimeField(null=True)
	cost = models.FloatField(default=0.0)
	pickup = models.BooleanField(default=False)
	complete = models.BooleanField(default=False)
	staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product, through='ProductOrder')

	def get_duration(self):
		if self.complete:
			return (self.time_out - self.time_in).total_seconds() // 60
		return (datetime.now(timezone.utc) - self.time_in).total_seconds()//60


class ProductOrder(models.Model):
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
	amount = models.IntegerField(default=1)