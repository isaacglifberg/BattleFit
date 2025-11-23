from rest_framework import generics, permissions, status
from .models import Battle
from .serializers import BattleSerializer
from rest_framework.response import Response


class BattleListCreateView(generics.ListCreateAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        return Battle.objects.filter(challenger=user) | Battle.objects.filter(opponent=user)

    
    def perform_create(self, serializer):
        serializer.save(challenger = self.request.user, status="pending")



class BattleAcceptView(generics.UpdateAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Battle.objects.all()

    def update(self, request, *args, **kwargs):
        battle = self.get_object()

        # Opponent ONLY
        if battle.opponent != request.user:
            return Response({"error": "Only the opponent can accept this battle."},
                            status=status.HTTP_403_FORBIDDEN)
        
        # Must be pending
        if battle.status != "pending":
            return Response({"error": "Battle is not pending."},
                            status=status.HTTP_400_BAD_REQUEST)
        

        # Accept challange
        battle.status = "active"
        battle.save()

        return Response(BattleSerializer(battle).data, status=status.HTTP_200_OK)      
    



class BattleDeclineView(generics.UpdateAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Battle.objects.all()

    def update(self, request, *args, **kwargs):
        battle = self.get_object()

        # Opponent ONLY
        if battle.opponent != request.user:
            return Response({"error": "Only the opponent can decline this battle."},
                            status=status.HTTP_403_FORBIDDEN)

        # Must be pending
        if battle.status != "pending":
            return Response({"error": "Battle is not pending."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Decline
        battle.status = "declined"
        battle.save()

        return Response(BattleSerializer(battle).data, status=status.HTTP_200_OK)


    