from django.db import models
from django.contrib.auth.models import User

class Battle(models.Model):
    CATEGORY_CHOICES = [
        ('pushups', 'Pushups'),
        ('pullups', 'Pullups'),
        ('bench_press', 'Bench Press'),
        ('run', 'Running'),
    ]

    GOAL_CHOICES = [
        ('max', 'Highest Value Wins'),
        ('min', 'Lowest Value Wins'),
        ('fastest', 'Fastest Time Wins'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('finished', 'Finished'),
    ]

    challenger = models.ForeignKey(User, related_name='challenger_battles', on_delete=models.CASCADE)
    opponent = models.ForeignKey(User, related_name='opponent_battles', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    winner = models.ForeignKey(User, related_name='won_battles', null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.challenger} vs {self.opponent} - {self.category} ({self.status})"
    

class EloRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1000)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"


