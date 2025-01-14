# Generated by Django 4.2.13 on 2024-06-14 20:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('fullName', models.CharField(max_length=100)),
                ('phoneNumber', models.CharField(blank=True, max_length=20, null=True)),
                ('codePostal', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Email')),
                ('role', models.CharField(choices=[('SUPER_ADMIN', 'Super Admin'), ('ADMIN', 'Admin'), ('CLIENT', 'Client')], max_length=11)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.personmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
