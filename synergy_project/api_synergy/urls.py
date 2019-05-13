from django.urls import path
from .views import UsersHandler, GroupsHanlder

urlpatterns = [
	path('', UsersHandler.as_view()),
	path('add_user/', UsersHandler.as_view()),
	path('edit_user/', UsersHandler.as_view()),
	path('delete_user/', UsersHandler.as_view()),
	path('groups/', GroupsHanlder.as_view()),
	path('add_group/', GroupsHanlder.as_view()),
	path('delete_group/', GroupsHanlder.as_view())
]