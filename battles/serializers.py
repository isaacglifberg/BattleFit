from rest_framework import serializers
from .models import Battle
from django.contrib.auth.models import User


class BattleSerializer(serializers.ModelSerializer):
    challenger = serializers.StringRelatedField(read_only=True)  
    opponent = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Battle
        fields = [
            'id',
            'challenger',
            'opponent',
            'category',
            'goal',
            'start_time',
            'end_time',
            'status',
            'winner',
            'created_at'
        ]
        read_only_fields = ['id', 'challenger', 'status', 'winner', 'created_at']
