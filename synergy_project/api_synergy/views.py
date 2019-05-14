from datetime import datetime
from .models import Users, Groups
from rest_framework.views import APIView
from rest_framework.response import Response


class UsersHandler(APIView):
	def get(self, request):
		count = Users.objects.count()
		users = [
			{'id': user.id, 'username': user.username, 'created': user.created,
			 'group': Groups.objects.filter(id=user.group_id_id)[0].name} for
			user in Users.objects.all()]
		return Response(users)

	def post(self, request):
		data = request.POST
		count = Users.objects.count()
		group_id = Groups.objects.filter(name=data['group'])[0].id
		new_user = Users(username=data['username'], created=datetime.utcnow(),
						 group_id_id=group_id, id=count + 1)
		new_user.save()
		return Response('Saved')

	def put(self, request):
		data = request.POST
		group_id = Groups.objects.filter(name=data['group'])[0].id
		Users.objects.filter(id=data['id']).update(username=data['username'],
												   group_id_id=group_id)
		return Response('Edited')

	def delete(self, request):
		data = request.POST
		user_id = data['id']
		Users.objects.filter(id=user_id).delete()
		return Response("Deleted")


class GroupsHanlder(APIView):
	def get(self, request):
		count = Groups.objects.count()
		groups = [
			{'id': group.id, 'name': group.name,
			 'description': group.description} for
			group in Groups.objects.all()]
		return Response(groups)

	def post(self, request):
		data = request.POST
		print(data)
		count = Groups.objects.count()
		new_group = Groups(name=data['name'], description=data['description'],
						   id=count + 1)
		new_group.save()
		return Response('Saved group')

	def put(self, request):
		data = request.POST
		Groups.objects.filter(id=data['id']).update(name=data['name'],
												   description=data['description'])
		return Response('Edited group')

	def delete(self, request):
		data = request.POST
		group_id = data['id']
		gr_has_users = Users.objects.filter(group_id_id=data['id']).count()
		if not gr_has_users:
			Groups.objects.filter(id=group_id).delete()
			return Response("Deleted group")
		return Response("Can't delete a group which has users")

