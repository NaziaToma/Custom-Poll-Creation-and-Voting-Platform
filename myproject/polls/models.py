from django.db import models
from django.utils import timezone  # Add this import
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  

    def __str__(self):
        return self.choice_text
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)  # Add this line
    country = models.CharField(max_length=100, default='Bangladesh')  # Default to Bangladesh
    district = models.CharField(max_length=100, default='Dhaka')
    #phone_number = PhoneNumberField()

    def __str__(self):
        return self.user.username

# Signal to create and save the profile when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()