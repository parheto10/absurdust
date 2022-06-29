from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Groupe, Sujet, Message, User
from django.db.models import Q
from .forms import GroupeForm, UserForm, UserCreationForm


# groupes = [
#     {'id':1, 'nom': "Attachement Fifa"},
#     {'id':2, 'nom': "Parlons Projets"},
#     {'id':3, 'nom': "Gaming"},
# ]

def connexion(request):
    page = 'Connexion'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Cet Utilisateur ne Figure pas das notre Base de Donnée, Réessayer !')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            dj_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Paramètres de Connexion Incorrect, Réessayer SVP !')

    ctx = {
        'page':page,
    }
    return render(request, 'gforce/connexion_inscription.html', ctx)

def deconnexion(request):
    logout(request)
    return redirect('home')

def inscription(request):
    # page = 'Inscription'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            dj_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Une Erreur est Survenue Réessayer SVP !!')
            # return redirect('inscription')

    ctx = {
        'form':form,
        # 'page':page,
    }

    return render(request, 'gforce/connexion_inscription.html', ctx)


def user_profile(request, pk):
    # user = User.objects.get(id=pk)
    user = get_object_or_404(User, id=pk)
    messages_goupes = user.message_set.all()
    salons = user.groupes.all()
    sujets = Sujet.objects.all()
    ctx = {
        'user':user,
        'salons':salons,
        'sujets':sujets,
        'messages_goupes':messages_goupes,
    }
    return render(request, 'gforce/profile.html', ctx)

@login_required(login_url='connexion')
def edit_user(requests):
    user = requests.user
    form = UserForm(instance=user)
    if requests.method == "POST":
        form = UserForm(requests.POST, requests.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)

    ctx = {
        'form': form,
    }
    return render(requests, 'gforce/edit-user.html', ctx)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') !=None else ''

    salons = Groupe.objects.filter(
        Q(sujet__nom__icontains=q) |
        Q(titre__icontains= q) |
        Q(description__icontains= q)
    )
    sujets = Sujet.objects.all().order_by('nom')[0:5]
    salon_count = salons.count()
    messages_goupes = Message.objects.filter(
        Q(groupe__sujet__nom__icontains=q)
    )[:5]

    ctx = {
        'salons': salons,
        'sujets': sujets,
        'salon_count': salon_count,
        'messages_goupes': messages_goupes,
    }
    return render(request, 'gforce/home.html', ctx)

def salon(request, pk):
    # groupe = Groupe.objects.get(id=pk)
    groupe = get_object_or_404(Groupe, id=pk)
    groupe_messages = groupe.message_set.all().order_by('-created_le')
    abonne_groupe = groupe.abonne_groupe.all()
    if request.method=='POST':
        message = Message.objects.create(
            user=request.user,
            groupe=groupe,
            contenu=request.POST.get('contenu')
        )
        groupe.abonne_groupe.add(request.user)
        return redirect('salons', pk=groupe.id)

    ctx = {
        'groupe': groupe,
        'groupe_messages': groupe_messages,
        'abonne_groupe': abonne_groupe,
    }

    return render(request, 'gforce/groupe.html', ctx)


@login_required(login_url='connexion')
def add_groupe(request):
    form = GroupeForm
    sujets = Sujet.objects.all()
    if request.method == 'POST':
        sujet_name = request.POST.get("sujet")
        sujet, created = Sujet.objects.get_or_create(nom=sujet_name)
        # form = GroupeForm(request.POST)
        Groupe.objects.create(
            hote=request.user,
            sujet=sujet,
            titre=request.POST.get('titre'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    ctx = {
        'form': form,
        'sujets': sujets,
    }
    return render(request, 'gforce/create-groupe.html', ctx)


@login_required(login_url='connexion')
def update_groupe(request, pk):
    groupe = get_object_or_404(Groupe, id=pk)
    # groupe = Groupe.objects.get(id=pk)
    form = GroupeForm(instance=groupe)
    sujets = Sujet.objects.all()

    if request.user != groupe.hote:
        return HttpResponse("Vous n'êtes pas l'auteur de ce groupe, impossible de le Modifier !")

    if request.method == 'POST':
        sujet_name = request.POST.get("sujet")
        sujet, created = Sujet.objects.get_or_create(nom=sujet_name)
        form = GroupeForm(request.POST, instance=groupe)
        groupe.titre = request.POST.get('titre')
        groupe.description = request.POST.get('description')
        groupe.sujet = sujet
        groupe.save()
        return redirect('home')
    ctx = {
        'form' : form,
        'sujets': sujets,
        'groupe' : groupe,
    }
    return render(request, 'gforce/create-groupe.html', ctx)


@login_required(login_url='connexion')
def delete_groupe(request, pk=None):
    obj = get_object_or_404(Groupe, id=pk)

    if request.user != obj.hote:
        HttpResponse("Vous n'êtes pas l'auteur de ce groupe, impossible de le Supprimer !")

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    ctx = {
        'obj': obj
    }
    return render(request, 'gforce/supprimer.html', ctx)


@login_required(login_url='connexion')
def delete_message(request, pk=None):
    obj = get_object_or_404(Message, id=pk)

    if request.user != obj.user:
        HttpResponse("Vous n'êtes pas l'auteur de ce groupe, impossible de le Supprimer !")

    if request.method == 'POST':
        obj.delete()
        return redirect('home')
    ctx = {
        'obj': obj
    }
    return render(request, 'gforce/supprimer.html', ctx)


def themes(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    thematiques = Sujet.objects.filter(
        nom__icontains=q
    )
    ctx = {
        'thematiques' : thematiques
    }
    return render(request, 'gforce/topics.html', ctx)

def activites(request):
    messages_goupes = Message.objects.all()
    ctx = {
        'messages_goupes':messages_goupes
    }
    return render(request, 'gforce/activites.html', ctx)
# Create your views here.
