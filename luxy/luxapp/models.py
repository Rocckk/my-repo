from djongo import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class Section(models.Model):
	kids = models.CharField(max_length=50)
	estate = models.CharField(max_length=50)
	transport = models.CharField(max_length=50)
	parts = models.CharField(max_length=50)
	add_id = models.ForeignKey(Ad, on_delete=True)

class Ad(models.Model):
	header = models.CharField(max_length=70)
	section_name = models.OneToOneField(Section, on_delete=True)
	description = models.CharField(max_length=9000)
	location = models.CharField()
	phone = models.IntegerField()
	email = models.EmailField()
	contact_person = models.CharField(max_length=20)


class Users(AbstractBaseUser):
	username = models.CharField(max_length=128)
	email = models.EmailField(max_length=50, unique=True)
	password = models.CharField(max_length=128)
	first_name = models.CharField(blank=True, max_length=30)
	last_name = models.CharField(blank=True, max_length=20)
	add_id = models.ForeignKey(Ad, on_delete=True)
	objects = BaseUserManager()
	USERNAME_FIELD = 'username'


