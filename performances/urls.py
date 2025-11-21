from django.urls import path
from .views import PerformanceCreateView

urlpatterns = [
    path('', PerformanceCreateView.as_view(), name='performance-list-create'),
]