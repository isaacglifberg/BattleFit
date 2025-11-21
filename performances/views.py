from rest_framework import generics, permissions
from .models import Performance
from .serializers import PerformanceSerializer

class PerformanceCreateView(generics.ListCreateAPIView):
    serializer_class = PerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Performance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
