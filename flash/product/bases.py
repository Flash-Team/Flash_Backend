from django.db import models


class BaseProduct(models.Model):
    """
    Abstract base for Product and Organization
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    logo = models.FileField(null=True, blank=True)
    sum = models.IntegerField(default=0)
    count = models.IntegerField(default=1)

    class Meta:
        abstract = True

    @property
    def rating(self):
        return self.sum / self.count
