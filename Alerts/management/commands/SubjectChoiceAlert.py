from django.core.management.base import BaseCommand
from Manage.models import Semester
from ...models import Alert
import datetime

class Command(BaseCommand):
    help = 'Cronjob'
    # This will be running in the morning
    def handle(self, *args, **options):
        today = datetime.datetime.today().date()
        # Get the subject chocie objects which deadline is tomorrow        
        semesters = Semester.objects.filter(subject_choice_deadline=today)        
        # for this we have to send alerts to the users        
        for semester in semesters:
            for subject_choises in semester.subjectchoices_set.filter(choices_locked=False):
                message_string = f"Friendly Reminder: Today is the deadline to mark your subject choices for the {semester.no} Semester. Please ensure that your selections are submitted by the end of the day. Thank you for your attention to this important step!"
                Alert.objects.create(profile=subject_choises.profile,message=message_string,type='subject_choice_deadline_alert')

        self.stdout.write('Subject choice alerts sent')