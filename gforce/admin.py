from django.contrib import admin

from .models import Groupe, Message, Sujet, User

admin.site.register(User)
admin.site.register(Groupe)
admin.site.register(Message)
admin.site.register(Sujet)

# Register your models here.
