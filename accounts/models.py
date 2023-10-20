from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)

    # Add custom fields here, if needed

    def __str__(self):
        return self.username
    
class Livre(models.Model):
    titre = models.CharField(max_length=100)
    prix = models.FloatField(default=0)
    description = models.TextField(null=True)
    image = models.FileField(upload_to="livre")
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='auteur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Acheter(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='livre')
    acheteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='acheteur')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    