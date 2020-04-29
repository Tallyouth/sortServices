from rest_framework import serializers
from api.models import ScoreTable

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreTable
        fields = "__all__"