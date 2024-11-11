from django.db import models
from SMARTROLL.GlobalUtils import generate_unique_hash
from StakeHolders.models import Profile
# Create your models here.

alert_status_choices = (
    ('unseen', 'Unseen'),
    ('seen', 'Seen')
)

alert_types = (
    ('subject_choice_alert', 'Subject Choice Alert'),
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