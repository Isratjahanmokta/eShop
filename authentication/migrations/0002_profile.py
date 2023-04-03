# Generated by Django 4.1.7 on 2023-03-31 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=264)),
                ('full_name', models.CharField(blank=True, max_length=264)),
                ('address', models.TextField(blank=True, max_length=300)),
                ('city', models.CharField(blank=True, max_length=40)),
                ('zipcode', models.CharField(blank=True, max_length=10)),
                ('country', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
