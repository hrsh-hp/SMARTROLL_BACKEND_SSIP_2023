from django.db import models
from Profile.models import Profile
import uuid
import time
from django.db.models.signals import post_delete
from django.dispatch import receiver
from SMARTROLL.GlobalUtils import generate_unique_hash

# Create your models here.

SUBSCRIPTION_TYPES = [
    ('lectures','Lectures'),
    ('alerts','Alerts')    
]

class NotificationSubscriptions(models.Model):
    subscription = models.JSONField(null=True,blank=True)
    subscription_type = models.CharField(max_length=10,choices = SUBSCRIPTION_TYPES ,null=True,blank=True)

class SuperAdmin(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)    
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(SuperAdmin, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.profile.email
    
class Admin(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)    
    slug = models.SlugField(unique=True, null=True, blank=True)
    web_push_subscription = models.ManyToManyField(NotificationSubscriptions,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Admin, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.profile.email

class Teacher(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)    
    teacher_code = models.CharField(max_length=10,unique=True)    
    web_push_subscription = models.ManyToManyField(NotificationSubscriptions,blank=True)
    is_active = models.BooleanField(default=False)
    seniority = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Teacher, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.profile.email if self.profile.email else self.profile.name
    
class Student(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
    enrollment  = models.CharField(max_length=12,unique=True)    
    slug = models.SlugField(unique=True, null=True, blank=True)
    sr_no = models.PositiveIntegerField(null=True,blank=True)
    web_push_subscription = models.ManyToManyField(NotificationSubscriptions,blank=True)
    is_active = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()                    
        super(Student, self).save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return f"{self.enrollment} | {self.profile.email if self.profile.email else self.profile.name}"

@receiver(post_delete, sender=Student)
def delete_related_profile(sender, instance, **kwargs):
    if instance.profile:
        instance.profile.delete()
