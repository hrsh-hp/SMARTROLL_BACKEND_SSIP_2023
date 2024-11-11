from django.core.management.base import BaseCommand
from Manage.models import SubjectChoices
from ...models import Alert
import datetime

class Command(BaseCommand):
    help = 'Cronjob'
    # This will be running in the morning
    def handle(self, *args, **options):
        today = datetime.datetime.today().date()
        # Get the subject chocie objects which deadline is tomorrow        
        objs = SubjectChoices.objects.filter(deadline_timestamp=today,choices_locked=False)
        # for this we have to send alerts to the users        
        for obj in objs:
            message_string = f"Friendly Reminder: Today is the deadline to mark your subject choices for the {obj.semester.no} Semester. Please ensure that your selections are submitted by the end of the day. Thank you for your attention to this important step!"
            Alert.objects.create(profile=obj.profile,message=message_string,type='subject_choice_alert')

        self.stdout.write('Subject choice alerts sent')