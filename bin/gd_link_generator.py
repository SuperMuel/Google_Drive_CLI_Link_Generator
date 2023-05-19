#!/usr/bin/env python3

import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import typer
from rich.console import Console

import json
import sys

__version__ = "0.1.0"

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

app = typer.Typer()
err_console = Console(stderr=True)


# Paths
project_folder = Path(__file__).resolve().parent.parent
config_path = project_folder / 'config.json'
credentials_path = project_folder / 'credentials.json'
token_path = project_folder / 'token.json'


def load_config():
    with open(config_path) as f:
        return json.load(f)


config = load_config()


def get_drive_service():
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)


def get_drive_id(service, name, parent_id):
    """
    Fetch the ID of a file or folder from Google Drive.

    Args:
        service (Resource): An instance of googleapiclient.discovery.Resource representing the Google Drive service.
        name (str): The name of the file or folder for which the ID is to be fetched.
        parent_id (str): The ID of the parent directory containing the file or folder.

    Returns:
        str: The ID of the file or folder if it exists. None otherwise.
    """
    response = service.files().list(q=f"'{parent_id}' in parents and name='{name}'",
                                    spaces='drive',
                                    fields='nextPageToken, files(id, name)').execute()
    for file in response.get('files', []):
        return file.get('id')


def get_file_id(service, gdrive_path, file_path):
    """
    Fetch the ID of a file or folder given its absolute path on the local system.

    Args:
        service (Resource): An instance of googleapiclient.discovery.Resource representing the Google Drive service.
        gdrive_path (Path): A pathlib.Path object representing the root of the Google Drive folder on the local system.
        file_path (Path): A pathlib.Path object representing the absolute path of the file or folder on the local system.

    Returns:
        str: The ID of the file or folder if it exists. None otherwise.
    """
    parts = Path(file_path).relative_to(gdrive_path).parts
    id = 'root'
    for part in parts:
        id = get_drive_id(service, part, id)
    return id


def create_permission(service, file_id, type, role):
    if type == 'user':
        permission = {
            'type': type,
            'role': role,
            'emailAddress': config['email']
        }
    else:
        permission = {
            'type': type,
            'role': role,
        }
    service.permissions().create(fileId=file_id, body=permission).execute()


@app.command()
def main(file_path: Path = typer.Argument(..., help="The path to the file or directory in Google Drive you want to share."),
         anyone: bool = typer.Option(False, '-a', '--anyone', help="If set, the share link will be accessible to anyone having the link.")):
    """
    Generates a share link for a file or directory in your Google Drive.
    The file or directory is specified by the file_path argument.
    By default, the share link is limited. Use the --anyone option to create a link that's accessible to anyone having the link.
    """
    gdrive_path = Path(config['gdrive_path']).expanduser()
    file_path = file_path.resolve()

    if not file_path.exists():
        err_console.print(
            f"'{file_path}' doesn't exist.")
        raise typer.Exit()

    if not gdrive_path in file_path.parents:
        err_console.print(
            f"'{file_path}' is not in the Google Drive folder, which is {config['gdrive_path']}")
        raise typer.Exit()

    service = get_drive_service()
    file_id = get_file_id(service, gdrive_path, file_path)

    if anyone:
        role = 'reader'
        type = 'anyone'
    else:
        role = 'writer'
        type = 'user'

    create_permission(service, file_id, type, role)
    result = service.files().get(fileId=file_id, fields='webViewLink').execute()

    link = typer.style(result['webViewLink'],
                       fg=typer.colors.BLUE, bold=True)
    typer.echo(link)


if __name__ == "__main__":
    app()
