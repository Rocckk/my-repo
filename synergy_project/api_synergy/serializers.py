from rest_framework import serializers

from .models import Users, Groups

class GroupsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Groups
		fields = ('id', 'name', 'description')

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = ('id', 'username', 'created', 'group_id')