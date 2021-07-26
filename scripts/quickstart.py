from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from software.Plant_eV.env_conditions import Sensors
from datetime import datetime
import time

S = Sensors()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive.metadata',
          'https://www.googleapis.com/auth/drive']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1rri--nBigNM81pKesh6lv49hO8oz41gK76Z_r3s0EVk'
SAMPLE_RANGE_NAME = 'Sheet1'

class Sheets_Logging():
#def main():

    def __init__(self):
       self.service = None
       self.credentials = self.auth()

    def auth(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service_sheet = build('sheets', 'v4', credentials=creds)

        self.service_drive = build('drive', 'v3', credentials=creds)

    def read_data(self):
        # Call the Sheets API
        service = self.service_sheet
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            # Print first column
            print('%s' % (values[0]))


    def write_data(self):
        # Write to the sheets API
        service = self.service_sheet
        rh, temp = S.rh_temp()
        co2, voc = S.gas()
        date = datetime.now()
        Data = [[str(date).split('.')[0],temp,rh,co2,voc,]]
        body = {
	     'values': Data
        }

        result = service.spreadsheets().values().append(
               spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
               valueInputOption='USER_ENTERED', body=body).execute()


    def send_image(self):
        #Send a image to the drive
        service       = self.service_drive
        folder_id     = '17c4i15J_1m_ONgt5HFr-SeEzdv49WUYb'
        path          = S.picture()
        file_metadata = {'name':[path],'parents':[folder_id]}
        media         = MediaFileUpload(path, mimetype='image/jpeg', resumable=True)
        file          = service.files().create(body=file_metadata,
                                               media_body=media,
                                               fields='id').execute()



if __name__ == '__main__':
    doc = Sheets_Logging()
    for j in range(30):
        doc.write_data()
        doc.send_image()
        print(j)
        time.sleep(120)
