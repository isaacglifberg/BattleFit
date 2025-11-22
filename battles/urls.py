from django.urls import path
from .views import BattleListCreateView


urlpatterns = [
    path('', BattleListCreateView.as_view(), name='battle-list-create'),
]