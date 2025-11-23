from django.urls import path
from .views import BattleListCreateView, BattleAcceptView, BattleDeclineView, BattleFinishView


urlpatterns = [
    path('', BattleListCreateView.as_view(), name='battle-list-create'),
    path('<int:pk>/accept/', BattleAcceptView.as_view(), name='battle-accept'),
    path('<int:pk>/decline/', BattleDeclineView.as_view(), name='battle-decline'),
    path('<int:pk>/finish/', BattleFinishView.as_view(), name='battle-finish')
]