# Generated by Django 2.1.1 on 2018-12-08 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_creation', models.DateField()),
                ('product', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=30)),
                ('LastName', models.CharField(max_length=30)),
                ('BirthDate', models.DateField()),
                ('RegistrationDate', models.DateField()),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='lux_app.Order')),
            ],
        ),
    ]
