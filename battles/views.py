from rest_framework import generics, permissions
from .models import Battle
from .serializers import BattleSerializer


class BattleListCreateView(generics.ListCreateAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Battle.objects.filter(challenger=user) | Battle.objects.filter(opponent=user)

    
    def perform_create(self, serializer):
        serializer.save(challenger = self.request.user, status="pending")
    