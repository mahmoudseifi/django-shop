# Generated by Django 4.2.14 on 2024-08-15 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_ordermodel_payment_alter_couponmodel_used_by_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordermodel',
            options={'ordering': ['-created_date']},
        ),
    ]
