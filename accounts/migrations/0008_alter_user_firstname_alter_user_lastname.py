# Generated by Django 4.1.5 on 2023-01-30 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='firstName',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='First name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastName',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Last name'),
        ),
    ]
