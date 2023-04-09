from django.db import models


class Address(models.Model):
    address = models.CharField(max_length=400)


class OsmTag(models.Model):
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.key}={self.value}"
