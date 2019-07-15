from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(null=False,max_length=254)
    is_register = models.BooleanField(null=False,default=False)
    host_name = models.CharField(max_length=254)
    ip = models.CharField(null=False,max_length=254)
    last_login = models.CharField(max_length=212)

    def __str__(self):
        return self.email


