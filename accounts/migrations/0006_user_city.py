# Generated by Django 4.1.5 on 2023-01-26 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_rename_firstname_user_firstname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='City'),
        ),
    ]
