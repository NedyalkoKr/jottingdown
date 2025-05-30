# Generated by Django 5.2 on 2025-04-15 20:42

import django.core.validators
import validators.account_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customuser',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'max_length': "Email address can't be more then 64 chars.", 'unique': 'User with this email already exists.'}, help_text='Your email will be used to activate the account and for password resets. So it has to be legit.', max_length=64, unique=True, validators=[validators.account_validators.validate_not_all_numbers]),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'max_length': "Username can't be bigger then 30 chars.", 'unique': 'User with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=3, message="Username can't be smaller then 3 chars.")]),
        ),
    ]
