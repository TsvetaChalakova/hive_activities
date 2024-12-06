import csv

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

user = get_user_model()


class Command(BaseCommand):
    help = "Import users from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            users_created = 0

            for row in reader:
                email = row['email']
                password = row['password']
                is_staff = row['is_staff'].lower() in ['true', '1', 'yes']
                is_superuser = row['is_superuser'].lower() in ['true', '1', 'yes']

                if not user.objects.filter(email=email).exists():
                    user.objects.create_user(
                        email=email,
                        password=password,
                        is_staff=is_staff,
                        is_superuser=is_superuser
                    )
                    users_created += 1

            self.stdout.write(self.style.SUCCESS(f"{users_created} users imported successfully."))
