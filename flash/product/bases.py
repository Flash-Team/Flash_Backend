from django.db import models


# Abstract class, base for Product and Organization (in future)
# Need to find appropriate name
class BaseProduct(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    logo = models.CharField(max_length=999)                         # indeed url field
    rating = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        abstract = True
