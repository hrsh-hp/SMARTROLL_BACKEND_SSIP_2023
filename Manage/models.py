from django.db import models
import time
import uuid
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from StakeHolders.models import Teacher,Student,Admin,SuperAdmin

# Create your models here.

def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash


class College(models.Model):
    college_name = models.CharField(max_length=255)    
    slug = models.SlugField(unique=True,null=True,blank=True)
    code = models.CharField(max_length=3)
    super_admins = models.ManyToManyField(SuperAdmin,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(College, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.college_name

class Term(models.Model):
    start_year = models.PositiveIntegerField(validators = [MinValueValidator(1900),MaxValueValidator(2100)],null=True,blank=True)
    end_year = models.PositiveIntegerField(validators = [MinValueValidator(1900),MaxValueValidator(2100)],null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)  
    college = models.ForeignKey(College,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Term, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Term - {self.start_year} | {self.end_year}"


class Branch(models.Model):
    branch_name = models.CharField(max_length=255)    
    admins = models.ManyToManyField(Admin,blank=True)
    teachers = models.ManyToManyField(Teacher,blank=True)
    term = models.ForeignKey(Term,on_delete=models.CASCADE,null=True,blank=True) 
    slug = models.SlugField(unique=True,null=True,blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Branch, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.branch_name} | {self.term}"

stream_choices = [
    ('BE',"Bachelor's"),
    ('ME',"Master's")
]

class Stream(models.Model):
    title = models.CharField(max_length=20,choices=stream_choices)
    stream_code = models.CharField(null=True,blank=True,max_length=3)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,blank=True)   
    slug = models.SlugField(unique=True,null=True,blank=True)

    class Meta:
        # Ensuring that stream_code is unique within a term, not globally.
        constraints = [
            models.UniqueConstraint(fields=['stream_code', 'branch'], name='unique_stream_code_in_term')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Stream, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Stream - {self.title} | {self.branch}"


class Semester(models.Model):
    no = models.IntegerField()    
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    stream = models.ForeignKey(Stream,on_delete=models.CASCADE,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Semester, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Semester - {self.no} | {self.stream}"
    
class Division(models.Model):
    division_name = models.CharField(max_length=2)
    slug = models.SlugField(unique=True,null=True,blank=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Division, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Division - {self.division_name} | {self.semester}"
    

class Batch(models.Model):
    batch_name = models.CharField(max_length=10)
    slug = models.SlugField(unique=True,null=True,blank=True)
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    students = models.ManyToManyField(Student,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Batch, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Batch - {self.batch_name} | {self.division}"
    
class PermanentSubject(models.Model):
    degree = models.CharField(max_length=20,null=True,blank=True)
    stream_code = models.CharField(max_length=20,null=True,blank=True)
    sem_year=models.PositiveIntegerField(null=True,blank=True)
    subject_code = models.CharField(max_length=20,null=True,blank=True)
    eff_from=models.CharField(max_length=20,null=True,blank=True)
    subject_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=20,null=True,blank=True)
    category = models.CharField(max_length=255,null=True,blank=True)    
    L=models.PositiveIntegerField(null=True,blank=True)    
    P=models.PositiveIntegerField(null=True,blank=True)
    T=models.PositiveIntegerField(null=True,blank=True)
    credit = models.FloatField(null=True,blank=True)
    E=models.PositiveIntegerField(null=True,blank=True)
    M=models.PositiveIntegerField(null=True,blank=True)
    I=models.PositiveIntegerField(null=True,blank=True)
    V=models.PositiveIntegerField(null=True,blank=True)
    total_marks = models.PositiveIntegerField(null=True,blank=True)
    is_elective=models.BooleanField(default=False)
    is_practical=models.BooleanField(default=False)
    is_theory=models.BooleanField(default=False)
    is_semipractical=models.BooleanField(default=False)
    is_functional=models.BooleanField(default=False)
    practical_exam_duration = models.CharField(max_length=20,null=True,blank=True)
    theory_exam_duration = models.CharField(max_length=20,null=True,blank=True)
    remark=models.TextField(null=True,blank=True)        
    slug = models.SlugField(unique=True,null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()                                
        super(PermanentSubject, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return f"{self.subject_name}"
    
class Subject(models.Model):
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,blank=True,null=True)
    included_batches = models.ManyToManyField(Batch,blank=True)    
    subject_map = models.ForeignKey(PermanentSubject,on_delete=models.CASCADE,blank=True,null=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()                                
        super(Subject, self).save(*args, **kwargs)
    

    def __str__(self) -> str:
        return f"{self.subject_map.subject_name} | {self.semester}"
    
class TimeTable(models.Model):
    division = models.ForeignKey(Division,on_delete=models.CASCADE)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(TimeTable, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"Division - {self.division}"
    
class GPSCoordinates(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    long = models.CharField(max_length=255,null=True,blank=True)
    latt = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self) -> str:
        return self.title if self.title else 'None'



class Classroom(models.Model):
    class_name = models.CharField(max_length = 20)    
    slug = models.SlugField(unique=True,null=True,blank=True)
    branch = models.ManyToManyField(Branch)
    gps_coordinates = models.ForeignKey(GPSCoordinates,blank=True,null=True,on_delete=models.DO_NOTHING)


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

class Schedule(models.Model):
    day = models.CharField(max_length=10,null=True,blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    timetable = models.ForeignKey(TimeTable,on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()            
        super(Schedule, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.day} | {self.timetable}"

class Lecture(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.CharField(max_length=6,choices=LECTURE_TYPE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, null=True,blank=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, null=True,blank=True)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE, null=True,blank=True)
    batches = models.ManyToManyField(Batch, blank=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.DO_NOTHING, null=True,blank=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    is_proxy = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Lecture, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.type} - {self.subject} - {self.schedule}"
    
class Link(models.Model):
    from_lecture = models.ForeignKey(Lecture, null=True, blank=True, on_delete=models.CASCADE, related_name='from_links')
    to_lecture = models.ForeignKey(Lecture, null=True, blank=True, on_delete=models.CASCADE, related_name='to_links')
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Link, self).save(*args, **kwargs)