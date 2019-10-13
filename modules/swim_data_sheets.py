from __future__ import print_function
import pickle
import os.path
import copy
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from swimmer import Swimmer
from swim import Swim
from event import Event

from sheet_id import SPREADSHEET_ID

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

sheetsAPI = None
sheets = None
valuesAPI = None

batch_requests_body_template = {
  "includeSpreadsheetInResponse": False,
  "requests": []
}

def AddCreateWorksheetToBatchRequests(name, id, numRows, numColumns, batch_requests_body):
  request = {
    "addSheet": {
      "properties": {
        "sheetType": "GRID",
        "title": name,
        "gridProperties": {
          "rowCount": numRows,
          "columnCount": numColumns
        }
      }
    }
  }
  if id is not None:
    # Use the specified id
    request["addSheet"]["properties"]["sheetId"] = id
  batch_requests_body["requests"].append(request)

def AddUpdateWorksheetPropertiesToBatchRequests(properties, batch_requests_body):
  request = {
    "updateSheetProperties": {
      "properties": properties,
      "fields": "*"
    }
  }
  batch_requests_body["requests"].append(request)

def AddDeleteWorksheetToBatchRequests(id, batch_requests_body):
  request = {
    "deleteSheet": {
      "sheetId": id
    }
  }
  batch_requests_body["requests"].append(request)
  
def GetWorksheet(id):
  global sheets
  worksheets = sheets['sheets']
  for sheet in worksheets:
    if sheet['properties']['sheetId'] == id:
      return sheet
  return None

def GetNumRowsInWorksheet(id):
  sheet = GetWorksheet(id)
  if sheet is not None:
    return sheet['properties']['gridProperties']['rowCount']
  return 0
  
def ConnectToSheets():
  global sheetsAPI
  global valuesAPI
  global sheets

  print('Loading Credentials')
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
      pickle.dump(creds, token)

  print('Building sheets API')
  service = build('sheets', 'v4', credentials=creds)

  # Get the APIs
  sheetsAPI = service.spreadsheets()
  valuesAPI = sheetsAPI.values()
  
  print('Getting sheet information')
  request = sheetsAPI.get(spreadsheetId=SPREADSHEET_ID)
  sheets = request.execute()
  print(sheets)

def FormatDate(date):
  return date.strftime("%d/%m/%Y")

def UpdateSwimmerData(swimmers):
  global valuesAPI
  ConnectToSheets()
  pass
  title_row = ["Date", "Event", "Meet", "Level", "Time", "Splits", "Id"]
  batch_requests_body = copy.deepcopy(batch_requests_body_template)
  batch_updates = []
  batch_updates_body = {
    "includeValuesInResponse": False,
    "data": batch_updates,
    "responseDateTimeRenderOption": "FORMATTED_STRING",
    "responseValueRenderOption": "UNFORMATTED_VALUE",
    "valueInputOption": "RAW"
  }
  sheets_to_keep = set()
  sheets_to_keep.add(0) # The index
  num_new_swimmers = 0
  for swimmer in swimmers:
    existing_num_rows = GetNumRowsInWorksheet(swimmer.asa_number)
    num_swims = len(swimmer.swims)
    
    # if existing_num_rows != 0:
      # sheet = GetWorksheet(swimmer.asa_number)
      # properties = sheet["properties"]
      # properties["title"] = str(swimmer.asa_number)
      # AddUpdateWorksheetPropertiesToBatchRequests(properties, batch_requests_body)
    
    if existing_num_rows == (num_swims + 1):
      print(swimmer.full_name() + " is already up to date.")
    else:
      print("Updating " + swimmer.full_name())
      if existing_num_rows == 0:
        num_new_swimmers = num_new_swimmers + 1
      else:
        # Delete the old worksheet for this swimmer
        AddDeleteWorksheetToBatchRequests(swimmer.asa_number, batch_requests_body)
      AddCreateWorksheetToBatchRequests(str(swimmer.asa_number), swimmer.asa_number, num_swims + 1, 7, batch_requests_body)
      rows = [title_row]
      for swim in swimmer.swims:
        row = [FormatDate(swim.date), swim.event.short_name(), swim.meet, swim.level, swim.race_time, None, None]
        rows.append(row)
      value_range_body = {
        "range": str(swimmer.asa_number) + '!A1',
        "majorDimension": "ROWS",
        "values": rows
      }
      batch_updates.append(value_range_body)

  # Now the index
  if (num_new_swimmers != 0):
    if GetWorksheet(0) is not None:
      AddDeleteWorksheetToBatchRequests(0, batch_requests_body)
    AddCreateWorksheetToBatchRequests("Index", 0, len(swimmers) + 1, 6, batch_requests_body)
    rows = [["seNumber", "firstName", "knownAs", "lastName", "gender", "dob"]]
    for swimmer in swimmers:
      gender = 'F'
      if swimmer.is_male:
        gender = 'M'
      row = [swimmer.asa_number, swimmer.first_name, swimmer.known_as, swimmer.last_name, gender, FormatDate(swimmer.date_of_birth)]
      rows.append(row)
      value_range_body = {
        "range": "Index!A1",
        "majorDimension": "ROWS",
        "values": rows
      }
      batch_updates.append(value_range_body)

  # Execute all the worksheet adds and deletes
  print("Executing sheet creation and deletion")
  if len(batch_requests_body["requests"]) > 0:
    request = sheetsAPI.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=batch_requests_body)
    response = request.execute()
  # Execute all the data updates
  print("Updating data")
  if len(batch_updates) > 0:
    request = valuesAPI.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=batch_updates_body)
    response = request.execute()
