from django.db import models

class Groups(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=300)


class Users(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	username = models.CharField(max_length=100)
	created = models.DateTimeField()
	group_id = models.ForeignKey('Groups', on_delete=models.CASCADE)