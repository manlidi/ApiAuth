from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username
    
class Livre(models.Model):
    titre = models.CharField(max_length=100)
    auteur = models.CharField(max_length=60)
    prix = models.FloatField(default=0)
    description = models.TextField(null=True)
    
