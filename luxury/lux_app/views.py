"""
This module handles API requests and returns necessary information in JSON format
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import User

# format for converting datetime objects into strings
FORMAT = '%Y-%m-%d'


@require_http_methods(["GET"])
def get_all_users(request):
	"""
	the function which accepts request and returns the list of all users as JSON
	"""
	list_of_users = [{'First Name': user.FirstName, 'Last Name': user.LastName,
					  'Birth Date': user.BirthDate.strftime(FORMAT),
					  'Registration date': user.RegistrationDate.strftime(FORMAT),
					  'Order': user.order} for user in User.objects.all()]
	return JsonResponse(list_of_users, status=200, safe=False)


@require_http_methods(["GET"])
def get_users_by_reg_date(request, year, month, day):
	"""
	function which handles incoming request with year, month and day of user's registration as
	keyword arguments and returns JSON with list of users/user who was/were registered on that
	date or 404 if not found
	"""
	requested_date = year + '-' + month + '-' + day
	users = [{'First Name': user.FirstName, 'Last Name': user.LastName,
			  'Birth Date': user.BirthDate.strftime(FORMAT),
			  'Registration date': user.RegistrationDate.strftime(FORMAT),
			  'Order': user.order} for user in User.objects.all() if
			 user.RegistrationDate.strftime(FORMAT) == requested_date]
	if users:
		return JsonResponse(users, status=200, safe=False)
	return HttpResponse('No such user', status=404)
