from rest_framework import serializers
from .models import Performance

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ['id', 'user', 'category', 'value', 'unit', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']