from rest_framework.serializers import ModelSerializer
from gforce.models import Groupe


class GroupeSerialize(ModelSerializer):
    class Meta:
        model = Groupe
        fields = '__all__'