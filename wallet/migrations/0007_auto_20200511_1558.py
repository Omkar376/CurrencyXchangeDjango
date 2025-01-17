# Generated by Django 3.0.6 on 2020-05-11 10:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0006_auto_20200509_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='receiver_amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('INR', 'Indian Rupee'), ('NZD', 'New Zealand Dollar'), ('GBP', 'Pound Sterling'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar'), ('JPY', 'Yen')], default='INR', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sender_amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('INR', 'Indian Rupee'), ('NZD', 'New Zealand Dollar'), ('GBP', 'Pound Sterling'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar'), ('JPY', 'Yen')], default='INR', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('AUD', 'Australian Dollar'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('INR', 'Indian Rupee'), ('NZD', 'New Zealand Dollar'), ('GBP', 'Pound Sterling'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('USD', 'US Dollar'), ('JPY', 'Yen')], default='INR', editable=False, max_length=3),
        ),
    ]
