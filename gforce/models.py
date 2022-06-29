from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nom = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Sujet(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return ('%s') %(self.nom)

class Groupe(models.Model):
    hote = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="groupes", null=True, blank=True)
    sujet = models.ForeignKey(Sujet, on_delete=models.SET_NULL, related_name="sujet_groupes", null=True, blank=True)
    titre = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    abonne_groupe = models.ManyToManyField(User, related_name='abonne_groupe')
    created_le = models.DateTimeField(auto_now_add=True)
    updated_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_le', '-created_le']

    def __str__(self):
        return ('%s') %(self.titre)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    contenu = models.TextField(null=True, blank=True)
    created_le = models.DateTimeField(auto_now_add=True)
    updated_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_le', '-created_le']

    def __str__(self):
        return ('%s') %(self.contenu[0:50])
#Create your models here.
