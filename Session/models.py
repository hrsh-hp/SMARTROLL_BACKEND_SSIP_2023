from django.db import models
from generate_mac import generate_mac
import hashlib
import secrets



# Create your models here.
def generate_random_unique_hash():
    # Generate a random string using secrets module
    random_string = secrets.token_hex(16)  # You can adjust the length as needed

    # Create a new SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the bytes-like object of the random string
    sha256.update(random_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hash_result = sha256.hexdigest()

    return hash_result

class Attendance(models.Model):
    student = models.ForeignKey('StakeHolders.Student',on_delete=models.DO_NOTHING)
    is_verified = models.BooleanField(default=False)
    physically_present = models.BooleanField(default=False)        


class Session(models.Model):
    session_id = models.TextField()
    total_students = models.ManyToManyField('StakeHolders.Student',blank=True)
    attendance = models.ManyToManyField(Attendance)
    present_student_count = models.IntegerField(blank=True,null=True)
    absent_student_count = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.session_id:
            self.session_id = generate_random_unique_hash()
            super(Session, self).save(*args, **kwargs)
        else:
            super(Session, self).save(*args, **kwargs)


