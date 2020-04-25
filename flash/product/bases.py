from django.db import models


# Abstract class, base for Product and Organization (in future)
class BaseProduct(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    logo = models.FileField(null=True, blank=True,)                         # indeed url field
    sum = models.IntegerField(default=0)
    count = models.IntegerField(default=1)

    class Meta:
        abstract = True

    @property
    def rating(self):
        return self.sum/self.count
