# Generated by Django 4.1.5 on 2023-01-26 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_firstname_alter_user_job_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='firstname',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='lastname',
            new_name='lastName',
        ),
    ]
