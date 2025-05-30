# Generated by Django 5.2 on 2025-04-17 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_followers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('deleted_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'deleted user',
                'verbose_name_plural': 'deleted users',
                'db_table': 'deleted_users',
            },
        ),
    ]
