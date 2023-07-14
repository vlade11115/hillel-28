import requests
from django.conf import settings
from django.db import models


# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    quantity = models.IntegerField()


class Order(models.Model):
    books = models.ManyToManyField(Book, through="OrderItem")
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, null=True)


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class MonoSettings(models.Model):
    public_key = models.CharField(max_length=200)

    @classmethod
    def get_token(cls):
        try:
            return cls.objects.last().public_key
        except AttributeError:
            key = requests.get(
                "https://api.monobank.ua/api/merchant/pubkey",
                headers={"X-Token": settings.MONOBANK_API_KEY},
            ).json()["key"]
            cls.objects.create(public_key=key)
            return key
