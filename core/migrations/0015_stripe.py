# Generated by Django 2.2.4 on 2019-11-01 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20191101_0440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stripe',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.Payment')),
                ('stripe_charge_id', models.CharField(max_length=50)),
            ],
            bases=('core.payment',),
        ),
    ]