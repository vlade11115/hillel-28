# Generated by Django 4.2.3 on 2023-07-14 16:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0002_order_alter_book_price_orderitem_order_books"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
