from django.db import models
import time
import uuid
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from StakeHolders.models import Teacher,Student,Admin

# Create your models here.

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

    
class Subject(models.Model):
    subject_name = models.CharField(max_length=255)
    code = models.IntegerField(unique=True)
    credit = models.IntegerField()
    slug = models.SlugField(unique=True,null=True,blank=True)
    teachers = models.ManyToManyField(Teacher)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()                                
        super(Subject, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return self.subject_name


class College(models.Model):
    college_name = models.CharField(max_length=255)    
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
            super(College, self).save(*args, **kwargs)
        else:
            super(College, self).save(*args, **kwargs)
            
    

    def __str__(self) -> str:
        return self.college_name

class Branch(models.Model):
    branch_name = models.CharField(max_length=255)    
    branch_code = models.IntegerField(unique=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    college = models.ForeignKey(College,on_delete=models.CASCADE)
    admins = models.ManyToManyField(Admin)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Branch, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.branch_name

class Semester(models.Model):
    no = models.IntegerField()    
    status = models.BooleanField(default=True)
    start_year = models.PositiveIntegerField(validators = [MinValueValidator(1900),MaxValueValidator(2100)])
    slug = models.SlugField(unique=True,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Semester, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Semester - {self.no}"
    
class Division(models.Model):
    division_name = models.CharField(max_length=2)
    slug = models.SlugField(unique=True,null=True,blank=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Division, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Division - {self.division_name}"
    

class Batch(models.Model):
    batch_name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True,null=True,blank=True)
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Batch, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Division - {self.batch_name}"
    

class TimeTable(models.Model):
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(TimeTable, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Division - {self.slug}"
    

class Schedule(models.Model):
    day = models.CharField(max_length=10,null=True,blank=True)    
    slug = models.SlugField(unique=True, null=True, blank=True)
    timetable = models.ForeignKey(TimeTable,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Schedule, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.day
    
class Router(models.Model):
    network_add = models.GenericIPAddressField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Router, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.network_add 

class Classroom(models.Model):
    class_name = models.CharField(max_length = 20)
    routers = models.ForeignKey(Router,on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Classroom, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.class_name


LECTURE_TYPE = [
        ('lab', 'Lab'),
        ('theory', 'Theory'),        
]
class Lecture(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=6,choices=LECTURE_TYPE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    batches = models.ManyToManyField(Batch)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Lecture, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.type} - {self.subject.subject_name}"



