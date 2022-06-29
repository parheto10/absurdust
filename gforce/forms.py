# from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Groupe, User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'nom',
            'username',
            'email',
            'password1',
            'password2'
        ]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'nom', 'avatar', 'bio']


class GroupeForm(ModelForm):
    class Meta:
        model = Groupe
        fields = '__all__'
        exclude = ['hote', 'abonne_groupe']
        # fields = [
        #     'titre',
        #     'sujet',
        #     'description'
        # ]