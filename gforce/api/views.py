from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GroupeSerialize

from gforce.models import Groupe


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/groupes',
        'GET /api/groupes/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getGroupes(request):
    groupes = Groupe.objects.all()
    serializer = GroupeSerialize(groupes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getGroupe(request, id=None):
    groupe = Groupe.objects.get(id=id)
    serializer = GroupeSerialize(groupe, many=False)
    return Response(serializer.data)