from rest_framework import serializers
from tributario.models import Negocio

class NegocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Negocio
        fields = '__all__'
