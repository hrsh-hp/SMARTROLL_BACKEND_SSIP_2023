from django.contrib import admin
from .models import Subject,College,Branch,Stream,Semester,Division,Batch,TimeTable,Schedule,Classroom,Lecture,Term,Link,GPSCoordinates,PermanentSubject,ComplementrySubjects,SubjectChoices

# Register your models here.

class ComonModelAdmin(admin.ModelAdmin):
    readonly_fields = ['slug'] 

admin.site.register(PermanentSubject,ComonModelAdmin)
admin.site.register(Subject,ComonModelAdmin)
admin.site.register(College,ComonModelAdmin)
admin.site.register(Branch,ComonModelAdmin)
admin.site.register(Stream,ComonModelAdmin)
admin.site.register(Semester,ComonModelAdmin)
admin.site.register(Division,ComonModelAdmin)
admin.site.register(Batch,ComonModelAdmin)
admin.site.register(TimeTable,ComonModelAdmin)
admin.site.register(Schedule,ComonModelAdmin)
admin.site.register(Classroom,ComonModelAdmin)
admin.site.register(Lecture,ComonModelAdmin)
admin.site.register(Term,ComonModelAdmin)
admin.site.register(Link,ComonModelAdmin)
admin.site.register(GPSCoordinates,ComonModelAdmin)
admin.site.register(ComplementrySubjects,ComonModelAdmin)
admin.site.register(SubjectChoices,ComonModelAdmin)