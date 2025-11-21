from django.db import models
from django.contrib.auth.models import User

class Performance(models.Model):
    CATEGORY_CHOICES = [
        ('pushups', 'Pushups'),
        ('pullups', 'Pullups'),
        ('bench_press', 'Bench Press'),
        ('squat', 'Squat'),
        ('deadlift', 'Deadlift'),
        ('run', 'Running'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    value = models.FloatField()  # ex: 100 kg, 50 reps, 5 km
    unit = models.CharField(max_length=20)  # "kg", "reps", "km"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}: {self.value} {self.unit}"

