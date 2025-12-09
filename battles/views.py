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


# View för att avsluta ett battle
class BattleFinishView(generics.UpdateAPIView):
    
    # Den serializer som används för att formatera utdata
    serializer_class = BattleSerializer
    
    # Endast inloggade användare får avsluta battles
    permission_classes = [permissions.IsAuthenticated]
    
    # Denna view ska jobba mot Battle-modellen
    queryset = Battle.objects.all()

    def update(self, request, *args, **kwargs):

        # Hämta battle-objektet baserat på pk från URL:en
        battle = self.get_object()

        if battle.status != "active":
            return Response({"error": "Battle is not active."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        from performances.models import Performance  # importera här för att undvika cirkulär import

        challenger_performance = Performance.objects.filter(
            user = battle.challenger,
            category = battle.category,
            timestamp_range = (battle.start_time, battle.end_time)

        )

        opponent_perf = Performance.objects.filter(
            user=battle.opponent,
            category=battle.category,
            timestamp__range=(battle.start_time, battle.end_time)
        )

        # Funktion som räknar totalpoängen för en viss användare
        def calculate_score(queryset, goal):
            if goal == "sum" or goal == "reps":
                return sum([p.reps for p in queryset])
            if goal == "weight":
                return sum([p.weight for p in queryset])
            return 0

        challenger_score = calculate_score(challenger_performance, battle.goal)
        opponent_score = calculate_score(opponent_perf, battle.goal)


        # Bestäm vinnare
        if challenger_score > opponent_score:
            battle.winner = battle.challenger
        elif opponent_score > challenger_score:
            battle.winner = battle.opponent
        else:
            battle.winner = None  # oavgjort

        battle.status = "finished"
        battle.save()

        data = BattleSerializer(battle).data
        data["challenger_score"] = challenger_score
        data["opponent_score"] = opponent_score


        

        return Response(data, status=status.HTTP_200_OK)


            






    