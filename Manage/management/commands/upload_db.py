import subprocess
from django.core.management.base import BaseCommand
import os
current_dir = os.path.dirname(__file__)
db_path = os.path.abspath(os.path.join(current_dir, "../../../db.sqlite3"))
class Command(BaseCommand):
    help = "Uploads the db.sqlite3 file to the specified EC2 instance"

    def handle(self, *args, **kwargs):
        # Define your SCP command
        scp_command = [
            "scp",
            "-i", "~/Downloads/SMARTROLL_SSIP_KEYPAIR.pem",  # Path to your key file
            db_path,  # Local path to the file you want to upload
            "ubuntu@ec2-50-17-207-10.compute-1.amazonaws.com:/home/ubuntu/db/db.sqlite3"  # Destination on the EC2 instance
        ]

        try:
            # Run the SCP command
            self.stdout.write("Uploading db.sqlite3 to EC2 instance...")
            result = subprocess.run(scp_command, check=True, capture_output=True, text=True)

            # Print success message
            self.stdout.write(self.style.SUCCESS("Database uploaded successfully!"))
            self.stdout.write(result.stdout)

        except subprocess.CalledProcessError as e:
            # Print error message
            self.stderr.write(self.style.ERROR("Failed to upload database"))
            self.stderr.write(e.stderr)
