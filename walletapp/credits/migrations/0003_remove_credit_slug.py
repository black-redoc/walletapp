# Generated by Django 4.1.4 on 2022-12-21 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("credits", "0002_credit_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="credit",
            name="slug",
        ),
    ]
