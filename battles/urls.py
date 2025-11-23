from django.urls import path
from .views import BattleListCreateView, BattleAcceptView, BattleDeclineView


urlpatterns = [
    path('', BattleListCreateView.as_view(), name='battle-list-create'),
    path('<int:pk>/accept/', BattleAcceptView.as_view(), name='battle-accept'),
    path('<int:pk>/decline/', BattleDeclineView.as_view(), name='battle-decline')
]