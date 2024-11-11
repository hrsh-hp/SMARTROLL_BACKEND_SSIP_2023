from .models import Batch, Division,Semester,Subject,Branch,College,TimeTable,Schedule,Lecture,Classroom,Term,Link,Stream,PermanentSubject
from datetime import datetime
from rest_framework import serializers
from Session.models import Session,Attendance

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['college_name','slug']

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['branch_name','slug']

class StreamSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()
    class Meta:
        model = Stream
        fields = ['title','stream_code','slug','branch']    
        

class DivisionSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Division
        fields = ['division_name','slug','full_name']
    
    def get_full_name(self,obj):
        return f"Division - {obj.division_name} | Sem - {obj.semester.no}"


class BatchSerializer(serializers.ModelSerializer):
    division = DivisionSerializer()
    class Meta:
        model = Batch
        fields = ['slug','batch_name','division']

class SemesterSerializer(serializers.ModelSerializer):    
    stream = StreamSerializer()
    class Meta:
        model = Semester
        fields = ['slug','no','status','stream']


class PermanentSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentSubject
        fields = ['stream_code','sem_year','subject_code','eff_from','subject_name','short_name','category','L','P','T','credit','E','M','I','V','total_marks','is_elective','is_practical','is_theory','is_semipractical','is_functional','practical_exam_duration','theory_exam_duration','remark','acedemic_year','slug']

class SemesterSerializerByStream(serializers.ModelSerializer):
    stream = StreamSerializer()
    subjects = serializers.SerializerMethodField()
    years = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = ['slug','no','status','stream','subjects','years']

    def __init__(self, years_arr=None, *args, **kwargs):
        super(SemesterSerializerByStream, self).__init__(*args, **kwargs)
        self.years_arr = years_arr
    
    def get_years(self,obj):
        return self.years_arr
    
    def get_subjects(self,obj):
        subject_set =  obj.subject_set.all()
        if not subject_set.exists():return None
        self.years_arr=None
        subject_maps = [subject.subject_map for subject in subject_set]
        subject_maps_serialized = PermanentSubjectSerializer(subject_maps,many=True)
        return subject_maps_serialized.data
        

class SubjectSerializer(serializers.ModelSerializer):
    semester = SemesterSerializer()
    included_batches = BatchSerializer(many=True)
    stream = serializers.SerializerMethodField()
    subject_map = PermanentSubjectSerializer()
    class Meta:
        model = Subject
        fields = ['subject_map','stream','semester','included_batches','slug']

    def get_stream(self,obj):
        return obj.semester.stream.title

class DivisionSerializerForTeacher(serializers.ModelSerializer):
    semester = SemesterSerializer()
    class Meta:
        model = Division
        fields = ['division_name','slug','semester']

class TermSerializer(serializers.ModelSerializer):    
    branches = serializers.SerializerMethodField()
    class Meta:
        model = Term
        fields = ['slug','start_year','end_year','type','status']

    def get_branches(self,obj):
        branches = obj.branch_set.all()
        branches_serialized = LectureSerializer(branches,many=True)
        return branches_serialized.data

class SemesterSerializerStudentCred(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    class Meta:
        model = Semester
        fields = ['slug','no','status','start_date','end_date','subjects','time_table']

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['class_name','slug']

class ScheduleSerializerForTeacher(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['day','slug','lectures']
    
    def __init__(self, teacher=None, *args, **kwargs):
        super(ScheduleSerializerForTeacher, self).__init__(*args, **kwargs)
        self.teacher = teacher
    
    def get_lectures(self,obj):
        lectures = obj.lecture_set.filter(teacher=self.teacher,is_active=True)
        lectures_serialized = LectureSerializer(lectures,many=True)
        return lectures_serialized.data
    
class ScheduleSerializerForStudent(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['day','slug','lectures']
    
    def __init__(self, batches=None,student=None,*args, **kwargs):
        super(ScheduleSerializerForStudent, self).__init__(*args, **kwargs)
        self.batches = batches
        self.student = student
    
    def get_lectures(self,obj):  
        lectures = obj.lecture_set.filter(batches__in=self.batches,is_active=True)        
        lectures_serialized = LectureSerializerForStudent(instance=lectures,student=self.student,many=True)
        return lectures_serialized.data        


class TimeTableSerializerForStudent(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()
    division = DivisionSerializerForTeacher()

    class Meta:
        model = TimeTable
        fields = ['slug','division','schedule']
    
    def __init__(self, batches,student=None,*args, **kwargs):
        super(TimeTableSerializerForStudent, self).__init__(*args, **kwargs)
        self.student = student
        self.batches = batches

    def get_schedule(self,obj):        
        current_datetime = datetime.now()
        current_day_name = current_datetime.strftime('%A')
        schedule = obj.schedule_set.filter(day=current_day_name.upper()).first()        
        if schedule:
            schedules_serialized = ScheduleSerializerForStudent(instance=schedule,student=self.student,batches=self.batches)
            return schedules_serialized.data    
        else:
            return None
    
class TimeTableSerializerForTeacher(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()    

    class Meta:
        model = TimeTable
        fields = ['slug','schedule']
    
    def __init__(self, teacher, *args, **kwargs):
        super(TimeTableSerializerForTeacher, self).__init__(*args, **kwargs)
        self.teacher = teacher

    def get_schedule(self,obj):        
        current_datetime = datetime.now()
        current_day_name = current_datetime.strftime('%A')
        schedule = obj.schedule_set.filter(day=current_day_name.upper()).first()
        # schedule = obj.schedule_set.filter(day='sunday')
        if schedule:
            schedules_serialized = ScheduleSerializerForTeacher(instance=schedule,teacher=self.teacher)
            return schedules_serialized.data    
        else:
            return None
    
class SessionSerializerForLecture(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['session_id','active','day','created_at']

class AttendanceSerializerStudentTimeTable(serializers.ModelSerializer):        
    class Meta:
        model = Attendance
        fields = ['is_present','marking_time']

class SessionSerializerForLectureForStudent(serializers.ModelSerializer):
    attendances = serializers.SerializerMethodField()
    class Meta:
        model = Session
        fields = ['session_id','active','day','created_at','attendances']
    
    def __init__(self,student=None,*args, **kwargs):
        super(SessionSerializerForLectureForStudent, self).__init__(*args, **kwargs)
        self.student = student

    def get_attendances(self,obj):                
        attendance_obj = obj.attendances.filter(student=self.student).first()        
        attendance_obj_serialized = AttendanceSerializerStudentTimeTable(instance=attendance_obj)
        return attendance_obj_serialized.data

class LectureSerializerForHistory(serializers.ModelSerializer):
    session = serializers.SerializerMethodField()
    classroom = serializers.SerializerMethodField()
    class Meta:
        model = Lecture
        fields = ['type','classroom','slug','session','is_active','is_proxy','start_time','end_time']
    
    def get_classroom(self,obj):
        return obj.classroom.class_name
    
    def get_session(self,obj):
        today= datetime.now().date()
        session_obj = obj.session_set.filter(active='post')
        session_serialized = SessionSerializerForLecture(session_obj,many=True)
        return session_serialized.data

class DivisionWiseTimeTableSerializer(serializers.ModelSerializer):
    timetable = serializers.SerializerMethodField()

    class Meta:
        model = Division
        fields = ['division_name','slug','timetable']
    
    def __init__(self, teacher, *args, **kwargs):
        super(DivisionWiseTimeTableSerializer, self).__init__(*args, **kwargs)
        self.teacher = teacher
    
    def get_timetable(self,obj):
        timetable = TimeTable.objects.filter(division=obj).first()        
        timetable_serialized = TimeTableSerializerForTeacher(instance=timetable,teacher=self.teacher)
        return timetable_serialized.data

class SemesterWiseTimeTableSerializer(serializers.ModelSerializer):
    divisions = serializers.SerializerMethodField()
    
    class Meta:
        model = Semester
        fields = ['slug','no','status','divisions']
    
    def __init__(self, teacher, *args, **kwargs):
        super(SemesterWiseTimeTableSerializer, self).__init__(*args, **kwargs)
        self.teacher = teacher
    
    def get_divisions(self,obj):
        divisions = Division.objects.filter(semester=obj)        
        divisions_serialized = DivisionWiseTimeTableSerializer(instance=divisions,many=True,teacher=self.teacher)
        return divisions_serialized.data

class StreamWiseTimeTableSerializer(serializers.ModelSerializer):
    semesters = serializers.SerializerMethodField()
    class Meta:
        model = Stream
        fields = ['title','slug','semesters']
    
    def __init__(self, teacher, *args, **kwargs):
        super(StreamWiseTimeTableSerializer, self).__init__(*args, **kwargs)
        self.teacher = teacher
    
    def get_semesters(self,obj):
        semesters = obj.semester_set.filter(status=True)
        semesters_serialized = SemesterWiseTimeTableSerializer(instance=semesters,many=True,teacher=self.teacher)
        return semesters_serialized.data

class BranchWiseTimeTableSerializer(serializers.ModelSerializer):
    streams = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        fields = ['branch_name','branch_code','slug','streams']
    
    def __init__(self, teacher, *args, **kwargs):
        super(BranchWiseTimeTableSerializer, self).__init__(*args, **kwargs)
        self.teacher = teacher
    
    def get_streams(self,obj):
        streams = obj.stream_set.all()
        streams_serialized = StreamWiseTimeTableSerializer(instance=streams,many=True,teacher=self.teacher)
        return streams_serialized.data

class BranchWiseTimeTableSerializerStudent(serializers.ModelSerializer):
    timetables = serializers.SerializerMethodField()
    stream = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        fields = ['stream','timetables']
    
    def __init__(self, student, *args, **kwargs):
        super(BranchWiseTimeTableSerializerStudent, self).__init__(*args, **kwargs)
        self.student = student

    def get_timetables(self,obj):
        batches = Batch.objects.filter(students=self.student,division__semester__stream__branch=obj)        
        division = Division.objects.filter(batch__students=self.student, batch__in=batches).first()
        timetables = TimeTable.objects.filter(division=division)        
        timetable_serialized = TimeTableSerializerForStudent(instance=timetables,student=self.student,batches=batches,many=True)
        return timetable_serialized.data

    def get_stream(self,obj):
        stream = obj.stream_set.first()
        stream_serialized = StreamSerializer(stream)
        return stream_serialized.data
    
class LectureSerializerForLink(serializers.ModelSerializer):
    subject = SubjectSerializer()
    class Meta:
        model = Lecture
        fields = ['start_time','end_time','type','subject']

class LinkSerializer(serializers.ModelSerializer):
    from_lecture  = LectureSerializerForLink()
    # to_lecture  = LectureSerializerForLink()
    class Meta:
        model = Link
        fields = ['from_lecture']
    
class LectureSerializer(serializers.ModelSerializer):
    session = serializers.SerializerMethodField()
    subject = SubjectSerializer()
    teacher = serializers.SerializerMethodField()
    classroom = ClassRoomSerializer()
    batches = BatchSerializer(many=True)
    link = serializers.SerializerMethodField()
    # survey = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ['start_time','end_time','type','subject','teacher','classroom','batches','slug','session','is_active','is_proxy','link']
    
    def get_link(self,obj):
        link = obj.to_links.all().filter(to_lecture=obj).first()
        if link:
            links_serialized = LinkSerializer(link)
            return links_serialized.data
        else:
            return None
        
    def get_teacher(self,obj):
        from StakeHolders.serializers import TeacherSerializer
        teacher_serialized = TeacherSerializer(obj.teacher)
        return teacher_serialized.data

    def get_session(self,obj):
        today= datetime.now().date()
        session_obj = obj.session_set.filter(day=today).first()
        session_serialized = SessionSerializerForLecture(session_obj)
        return session_serialized.data
    
    # def get_survey(self,obj):
    #     survey = obj.survey_set.all()        
    #     from Session.serializers import SurveySerializer
    #     survey_serialized = SurveySerializer(survey,many=True)
    #     return survey_serialized.data


class LectureSerializerForStudent(serializers.ModelSerializer):
    session = serializers.SerializerMethodField()
    subject = SubjectSerializer()
    teacher = serializers.SerializerMethodField()
    classroom = ClassRoomSerializer()
    batches = BatchSerializer(many=True)
    link = serializers.SerializerMethodField()
    # survey = serializers.SerializerMethodField()

    def get_link(self,obj):
        link = obj.to_links.all().filter(to_lecture=obj).first()
        if link:
            links_serialized = LinkSerializer(link)
            return links_serialized.data
        else:
            return None
        
    class Meta:
        model = Lecture
        fields = ['start_time','end_time','type','subject','teacher','classroom','batches','slug','session','is_active','is_proxy','link']
    
    def __init__(self,student=None,*args, **kwargs):
        super(LectureSerializerForStudent, self).__init__(*args, **kwargs)
        self.student = student

    def get_teacher(self,obj):
        return obj.teacher.profile.name

    def get_session(self,obj):
        today= datetime.now().date()
        session_obj = obj.session_set.filter(day=today).first()
        session_serialized = SessionSerializerForLectureForStudent(instance=session_obj,student=self.student)
        return session_serialized.data
    
    # def get_survey(self,obj):
    #     survey = obj.survey_set.filter(active=True).first()
    #     if not survey: return None
    #     from Session.serializers import SurveySerializer
    #     survey_serialized = SurveySerializer(survey)
    #     return survey_serialized.data


class ScheduleSerializer(serializers.ModelSerializer):
    lectures = serializers.SerializerMethodField()
    class Meta:
        model = Schedule
        fields = ['day','slug','lectures']

    def get_lectures(self,obj):
        lectures = obj.lecture_set.all().filter(is_active=True).order_by('start_time')
        lectures_serialized = LectureSerializer(lectures,many=True)
        return lectures_serialized.data

class TimeTableSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField()
    division = DivisionSerializer()

    class Meta:
        model = TimeTable
        fields = ['slug','division','schedules']

    def get_schedules(self,obj):
        schedules = obj.schedule_set.all()
        schedules_serialized = ScheduleSerializer(schedules,many=True)
        return schedules_serialized.data