"""
module which deals with models' admin integration with admin and enables importing and exporting
information from and into the database from csv and other files
"""
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import User


class UserResource(resources.ModelResource):
    """class which turns a model into the resource to be able to import information from csv file
    into database;
    widgets of the columns 'BirthDate' and 'RegistrationDate' are overridden to provide a correct
    format for imported dates, as the default widget lacks the needed format
    """
    class Meta:
        model = User
        exclude = ('id', 'order')
        import_id_fields = ['FirstName']
        # widgets of the columns 'BirthDate' and 'RegistrationDate' are overridden to provide a
        # correct format for imported dates, as the default widget lacks the needed format
        widgets = {'BirthDate': {'format': "%Y/%m/%d"}, 'RegistrationDate': {'format': "%Y/%m/%d"}}


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    """class which integrates UserResoure with Django Admin"""
    resource_class = UserResource


admin.site.register(User, UserAdmin)
