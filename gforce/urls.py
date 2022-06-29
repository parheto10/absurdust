from django.urls import path, include

from .views import (
    home,
    salon,
    add_groupe,
    update_groupe,
    delete_groupe,
    connexion,
    inscription,
    deconnexion,
    delete_message,
    user_profile,
    edit_user,
    themes,
    activites
)

urlpatterns = [
    path('connexion/', connexion, name='connexion'),
    path('profile/<str:pk>/', user_profile, name='user_profile'),
    path('edit_profile/', edit_user, name='edit_user'),
    path('inscription/', inscription, name='inscription'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('', home, name='home'),
    path('salons/<str:pk>/', salon, name='salons'),
    path('themes/', themes, name='themes'),
    path('activites/', activites, name='activites'),
    path('add_groupe/', add_groupe, name='add_groupe'),
    path('update_groupe/<str:pk>/', update_groupe, name='update_groupe'),
    path('delete_groupe/<str:pk>/', delete_groupe, name='delete_groupe'),
    path('delete_message/<str:pk>/', delete_message, name='delete_message'),
]