# Generated by Django 2.2.4 on 2019-11-01 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_stripe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='robo',
            options={'verbose_name': 'Уведомление об успешном платеже', 'verbose_name_plural': 'Уведомления об успешных платежах (ROBOKASSA)'},
        ),
    ]
