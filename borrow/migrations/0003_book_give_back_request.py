# Generated by Django 4.1.7 on 2023-07-19 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0002_book_give_back'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='give_back_request',
            field=models.BooleanField(default=False),
        ),
    ]