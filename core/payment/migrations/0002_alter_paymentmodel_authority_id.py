# Generated by Django 4.2.14 on 2024-08-12 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmodel',
            name='authority_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
