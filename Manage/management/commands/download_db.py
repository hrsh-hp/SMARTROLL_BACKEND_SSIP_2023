# your_app/management/commands/download_db.py

from django.core.management.base import BaseCommand
import subprocess
import os
current_dir = os.path.dirname(__file__)
db_path = os.path.abspath(os.path.join(current_dir, "../../../db.sqlite3"))

class Command(BaseCommand):
    help = 'Downloads the db.sqlite3 file from the EC2 instance'

    def handle(self, *args, **options):
        scp_command = [
            "scp",
            "-i", "~/Downloads/SMARTROLL_SSIP_KEYPAIR.pem",  # Path to your key file
            "ubuntu@ec2-50-17-207-10.compute-1.amazonaws.com:/home/ubuntu/db/db.sqlite3",  # Remote path on the EC2 instance
            db_path # Local path to save the file
        ]
        
        try:
            self.stdout.write("Downloading db.sqlite3 from EC2 instance...")
            result = subprocess.run(scp_command, check=True, capture_output=True, text=True)
            self.stdout.write("Database downloaded successfully.")
            self.stdout.write(result.stdout)
        except subprocess.CalledProcessError as e:
            self.stdout.write("Failed to download the database file.")
            self.stdout.write(e.stderr)
