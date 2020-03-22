from django.db import models


# Abstract class, base for Product and Organization (in future)
# Need to find appropriate name
class QWE(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    logo = models.CharField(max_length=999)
    rating = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=30)

#Added max_digits to price & commented organization field
class Product(QWE):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Foreign key for None because there is no model for organizations
    # organization = models.ForeignKey(None, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
