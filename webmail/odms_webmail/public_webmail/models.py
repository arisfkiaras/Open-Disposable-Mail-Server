from django.db import models

# Create your models here.
class Domain(models.Model):
    hostname = models.CharField(max_length=200)
       
    def __str__(self):
        return self.hostname