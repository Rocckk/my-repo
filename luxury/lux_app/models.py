from django.db import models


class Order(models.Model):
	date_of_creation = models.DateField()
	product = models.CharField(max_length=50)


class User(models.Model):
	FirstName = models.CharField(max_length=30)
	LastName = models.CharField(max_length=30)
	BirthDate = models.DateField()
	RegistrationDate = models.DateField()
	order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True)
