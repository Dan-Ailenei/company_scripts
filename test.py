import datetime
from pathlib import Path

import pytest

from google_client import get_files_client
from main import archive_files, get_next_month, get_last_day_of_last_month

BASE_DIR = Path(__file__).resolve(strict=True).parent


@pytest.fixture
def test_files_dir(tmp_path):
    files_dir = tmp_path / 'test_files'
    files_dir.mkdir()
    (files_dir / 'file1.txt').touch()
    (files_dir / 'file2.png').touch()

    yield files_dir


def test_archive_files_creates_archive_containing_all_files_when_called_with_files(test_files_dir, tmp_path):

    archive = archive_files('archive_dir', test_files_dir, test_files_dir.parent / 'test_archives')

    assert archive.exists()
    assert archive.name.endswith('zip')


def test_archive_files_creates_archive_dir_if_it_does_not_exist(test_files_dir):
    archives_dir = test_files_dir.parent / 'archives_directory'

    archive_path = archive_files('archive_dir', test_files_dir, archives_dir)

    assert archives_dir.exists()
    assert archives_dir.joinpath(archive_path.name).exists()


@pytest.mark.skip('this is just a simulation, if you run it you need to clean it up so skip it')
def test_gather_files_archive_and_send_through_email_for_12_months():
    today = get_next_month(datetime.date.today())
    files_client = get_files_client()

    for _ in range(12):
        last_month_string = get_last_day_of_last_month(today).strftime('%B-%Y')
        next_month_string = get_next_month(today).strftime('%B-%Y')

        # now = today.strftime("%d-%B-%Y")
        # archive_name = f"payments-{now}"
        #
        # gather_files_archive_and_send_through_email(archive_name, last_month_string, next_month_string)
        #
        # today = get_next_month(today)


        # CLEANUP
        # today = get_next_month(datetime.date.today())
        #
        # month_folder_response = files_client.list(
        #     q=f"name = '{last_month_string}'"
        # ).execute()
        #
        # for file in month_folder_response['files']:
        #     try:
        #         files_client.delete(fileId=file['id']).execute()
        #     except:
        #         pass
        # print(month_folder_response['files'])
        #
        # today = get_next_month(today)
        #
