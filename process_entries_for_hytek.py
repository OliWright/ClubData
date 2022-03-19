# Things to configure go here...
course_code = 'L'
csv_file_name = 'C:\\Users\\Sue\\Downloads\\2022-03-19_1018-Swansea_Aquatics_May_LC_Meet-entries.csv'
qualifying_window_start_str = '1/1/2021'
qualifying_window_end_str = '1/1/2050'
allow_conversions = True

import sys
sys.path.append("modules")
sys.path.append("qualifying_times")

import math
import helpers
from swim import Swim
from swimmer import Swimmer
from race_time import RaceTime
from event import Event

from read_csv_with_header import read_csv_with_header

# Read the swim list and process the swimmers
import read_club_rankings
swimmers = read_club_rankings.ReadClubRankingsFiles()

# Build a dictionary to lookup asa numbers to swimmers
asa_number_to_swimmer = {}
for swimmer in swimmers:
  asa_number_to_swimmer[swimmer.asa_number] = swimmer

# Read the swimming-events CSV file
entries = read_csv_with_header(csv_file_name)

qualifying_window_start = helpers.ParseDate_dmY(qualifying_window_start_str)
qualifying_window_end = helpers.ParseDate_dmY(qualifying_window_end_str)
def find_pb(event, swims):
  global allow_conversions
  global course_code
  global qualifying_window_start
  global qualifying_window_end
  best_time = None
  for swim in swims:
    swim_is_valid = (event.get_short_course_event_code() == swim.event.get_short_course_event_code())
    swim_course_code = swim.event.to_asa_course_code()
    if swim_is_valid and not allow_conversions:
      swim_is_valid = (course_code == swim_course_code)
    if swim_is_valid:
      swim_is_valid = (swim.date >= qualifying_window_start) and (swim.date <= qualifying_window_end)
    if swim_is_valid:
      #print("X")
      if (course_code == swim_course_code):
        race_time = swim.race_time
      else:
        race_time = swim.event.convert_time(swim.race_time)
        # Round to 0.1
        race_time = math.floor((race_time * 10) + 0.5) * 0.1
      if (best_time is None) or (race_time < best_time):
        best_time = race_time
  return RaceTime(best_time)

class RaceEntry():
  def __init__(self, swimmer, csv_entry):
    # Parse the event name string
    self.event = Event.create_from_long_event_str(csv_entry['Event'], course_code)
    self.time = RaceTime(csv_entry['Entry-Time'])
    self.pb = find_pb(self.event, swimmer.swims)

# Object for a swimmer entering the gala, containing an array of their entries
class EnteringSwimmer():
  def __init__(self, swimmer):
    self.swimmer = swimmer
    self.entries = []

# Process the entries
entering_swimmers = {}
num_entries = len(entries)
for entry in entries:
  asa_number = int( entry['ASA-Number'] )
  swimmer = asa_number_to_swimmer[asa_number]
  entering_swimmer = entering_swimmers.get(asa_number)
  if entering_swimmer is None:
    entering_swimmer = EnteringSwimmer(swimmer)
    entering_swimmers[asa_number] = entering_swimmer
  entering_swimmer.entries.append(RaceEntry(swimmer, entry))

# Output the data in a friendly fashion
print('\n\n---------------------------')
print('Swimmers:')
print('---------------------------')
for asa_number, entering_swimmer in entering_swimmers.items():
  swimmer = entering_swimmer.swimmer
  print('{name}\n\tSwim England #: {asa_number}\n\tDate of Birth: {dob}'.format(name = swimmer.full_name(), asa_number = swimmer.asa_number, dob = swimmer.date_of_birth_str()))

print('\n\n---------------------------')
print('Events:')
print('---------------------------')
for asa_number, entering_swimmer in entering_swimmers.items():
  swimmer = entering_swimmer.swimmer
  print('{name}'.format(name = swimmer.full_name()))
  for entry in entering_swimmer.entries:
    pb_str = '-'
    if entry.pb is not None:
      pb_str = str(entry.pb)
    print('\t{event}: Entry-Time: {time}, PB: {pb}'.format(event = entry.event.short_name_without_course(), time = str(entry.time), pb = pb_str))
