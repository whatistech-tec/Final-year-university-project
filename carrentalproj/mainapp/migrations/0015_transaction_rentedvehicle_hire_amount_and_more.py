# Generated by Django 4.2.20 on 2025-03-19 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_usersinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('checkout_id', models.CharField(max_length=100, unique=True)),
                ('mpesa_code', models.CharField(max_length=100, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('status', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='rentedvehicle',
            name='hire_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='rentedvehicle',
            name='status',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='rentedvehicle',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
