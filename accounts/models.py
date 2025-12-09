from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Den lagrar extra info som inte ligger i default User-modellen
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # ELO-rating startar på 1000 för alla
    elo_rating = models.IntegerField(default=1000)

    def __str__(self):
        return f"{self.user.username} (ELO: {self.elo_rating})"
    














# Detta körs varje gång en User skapas
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Detta säkerställer att profil sparas när user sparas
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

