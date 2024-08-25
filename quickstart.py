import os
import io
import google.auth
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive']

user_credentials = None

def create_local_folder():
	save_folder = os.path.join(os.getcwd(), 'All ODs')
	if not os.path.exists(save_folder):
		os.mkdir(save_folder)
	return save_folder

def authorize():
	"""Authorize user and store tokens, credentials if first time."""
	global user_credentials

	if os.path.exists("token.json"):
		user_credentials = Credentials.from_authorized_user_file("token.json", SCOPES)

	if not user_credentials or not user_credentials.valid:
		if (
			user_credentials
			and user_credentials.expired
			and user_credentials.refresh_token
		):
			user_credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
			user_credentials = flow.run_local_server(port=0)
		with open("token.json", "w") as token:
			token.write(user_credentials.to_json())


def search_file(query):
	"""Search file in drive location"""
	global user_credentials

	try:
		service = build("drive", "v3", credentials=user_credentials)
		files = []
		page_token = None
		while True:
			response = (
				service.files()
				.list(
					q=query,
					spaces="drive",
					fields="nextPageToken, files(id, name, webContentLink)",
					pageToken=page_token,
				)
				.execute()
			)
			# for file in response.get("files", []):
				# print(f'Found: {file.get("name")}, {file.get("id")}')
				# print(file)
			files.extend(response.get("files", []))
			page_token = response.get("nextPageToken", None)
			if page_token is None:
				break

	except HttpError as error:
		print(f"An error occurred: {error}")
		files = None

	return files


def export_pdf(file_obj):
	"""Download a Document file in PDF format.
	Args: 
		file_id : file ID of any workspace document format file
	Returns : IO object with location
	"""
	global user_credentials
	try:
		service = build("drive", "v3", credentials=user_credentials)
		request = service.files().get_media(fileId=file_obj.get('id'))
		file = io.BytesIO()
		downloader = MediaIoBaseDownload(file, request)
		done = False
		print("Downloading: ")
		while done is False:
			status, done = downloader.next_chunk()
			print(f"{int(status.progress() * 100)}", end=' ')

	except HttpError as error:
		print(f"An error occurred: {error}")
		file = None
	file_path = os.path.join(os.getcwd(), file_obj.get('name'))
	with open(file_path, 'wb') as bin_file:
		bin_file.write(file.getvalue())
	return f"Downloaded file {file_obj.get('name')}"

def main():
	authorize()
	folder = search_file("name = 'Placements OD List' and mimeType = 'application/vnd.google-apps.folder'")[0]
	files = search_file(f"'{folder.get('id')}' in parents and mimeType != 'application/vnd.google-apps.folder'")
	create_local_folder()
	export_pdf(files[0].get('id'), files[0].get('name'))

if __name__ == "__main__":
	main()
