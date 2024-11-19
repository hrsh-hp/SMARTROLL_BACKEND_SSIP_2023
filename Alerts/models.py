from django.db import models
from SMARTROLL.GlobalUtils import generate_unique_hash
from StakeHolders.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

alert_status_choices = (
    ('unseen', 'Unseen'),
    ('seen', 'Seen')
)

alert_types = (
    ('subject_choice_alert', 'Subject Choice Alert'),
    ('subject_deletion_alert', 'Subject Deletion Alert'),
    ('subject_choice_deadline_alert', 'Subject Choice Deadline Alert'),
    ('subject_choice_reset_alert', 'Subject Choice Reset Alert'),
)

class Alert(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=alert_status_choices,default='unseen')
    type = models.CharField(max_length=255,choices=alert_types)
    message = models.TextField()
    slug = models.SlugField(unique=True, null=True, blank=True)
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Alert, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.profile.name} | {self.status}"

@receiver(post_save, sender=Alert)
def save_user_profile(sender, instance, **kwargs):
    print(instance)