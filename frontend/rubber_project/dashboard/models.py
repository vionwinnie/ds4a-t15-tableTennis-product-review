from django.db import models

from django.db import models


class Order(models.Model):
    product_brand = models.CharField(max_length=40)
    rubber_name = models.CharField(max_length=100)
    overall_score = models.DecimalField(max_digits=5,decimal_places=2)
    comment = models.CharField(max_length=500)
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)
    # Create your models here.
