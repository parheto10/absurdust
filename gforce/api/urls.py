from django.urls import path
from .views import getRoutes, getGroupes, getGroupe

urlpatterns = [
    path('', getRoutes),
    path('groupes/', getGroupes),
    path('groupes/<str:id>', getGroupe),
]