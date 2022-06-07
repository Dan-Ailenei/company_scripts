import datetime
import os
import shutil
from distutils.archive_util import make_archive
from pathlib import Path
import calendar

from email_utils import send_email, gmail_user
from google_client import get_files_client

BASE_DIR = Path(__file__).resolve(strict=True).parent


def get_last_day_of_last_month(date):
    first_day_of_month = date.replace(day=1)
    return first_day_of_month - datetime.timedelta(days=1)


def get_next_month(date):
    year, month = calendar._nextmonth(year=date.year, month=date.month)
    return datetime.date(year=year, month=month, day=1)


class GoogleDriveController:
    def __init__(self):
        self.files_client = get_files_client()

    def get_files_from_directory(self, directory_name):
        month_folder_response = self.files_client.list(
            q=f"name = '{directory_name}'"
        ).execute()

        month_folder_id = month_folder_response["files"][0]["id"]
        results = self.files_client.list(q=f"'{month_folder_id}' in parents").execute()
        return results['files']

    def download_files(self, files, dest):
        for file in files:
            response = self.files_client.get_media(fileId=file["id"]).execute()
            (dest / file["name"]).write_bytes(response)

    def gather_files_from_dir(self, dir_name):
        files = self.get_files_from_directory(dir_name)

        dest = Path('month_files')
        if os.path.exists(dest) is False:
            dest.mkdir()

        dest /= dir_name
        dest.mkdir()

        self.download_files(files, dest)

        return dest

    def create_dir(self, dir_name, dest):
        file_metadata = {
            'name': dir_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [dest['id']]
        }
        self.files_client.create(body=file_metadata).execute()

    def get_main_root_directory(self):
        return self.files_client.list(
            q=f"name = 'Facturi-plati'"
        ).execute()['files'][0]


def archive_files(archive_name, files_dir, dest):
    filename = make_archive(archive_name, "zip", root_dir=files_dir)
    if dest.exists() is False:
        dest.mkdir()

    archive_path = Path(filename)
    shutil.move(str(archive_path), str(dest))

    return dest / archive_path.name


def send_archive_to_accountant(archive):
    accountant_email = 'aileneidan@yahoo.com'
    print(f'Sending archive {archive} to accountant {accountant_email}')
    send_email(gmail_user, [accountant_email], 'Facturi/plati', 'Facturile pe luna asta', files=[archive])


def gather_files_archive_and_send_through_email(archive_name, last_month_string, next_month_string):
    drive_controller = GoogleDriveController()

    print(f'Downloading files from google drive from {last_month_string}')
    files_dir_path = drive_controller.gather_files_from_dir(last_month_string)

    print(f'Creating directory {next_month_string}')
    drive_controller.create_dir(next_month_string, drive_controller.get_main_root_directory())

    print(f'Archiving files from {files_dir_path} to {archive_name}')
    archive = archive_files(archive_name, files_dir_path, Path("archived_dir"))

    send_archive_to_accountant(archive)


def main():
    today = datetime.date.today()

    last_month_string = get_last_day_of_last_month(today).strftime('%B-%Y')
    next_month_string = get_next_month(today).strftime('%B-%Y')

    now = today.strftime("%d-%B-%Y")
    archive_name = f"payments-{now}"

    gather_files_archive_and_send_through_email(archive_name, last_month_string, next_month_string)


if __name__ == "__main__":
    main()
