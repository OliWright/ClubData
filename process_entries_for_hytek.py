# Things to configure go here...
course_code = 'S'
csv_file_name = 'C:\\Users\\Sue\\Downloads\\2022-06-13_1911-Len_Thomas_Memorial_Meet-entries.csv'
qualifying_window_start_str = '1/1/2019'
qualifying_window_end_str = '1/1/2050'
allow_conversions = True
male_event_order = [
  "200 IM",
  "100 Breast",
  "50 Free",
  "100 Back",
  "50 Fly",
  "50 Back",
  "100 Fly",
  "50 Breast",
  "100 Free",
]

female_event_order = [
  "50 Back",
  "100 Fly",
  "50 Breast",
  "100 Free",
  "200 IM",
  "100 Breast",
  "50 Free",
  "100 Back",
  "50 Fly",
]

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

def init_event_to_order_score(event_order):
  event_code_to_order_score = {}
  score = 0
  for event_name in event_order:
    event = Event.create_from_str(event_name, course_code)
    event_code_to_order_score[event.event_code] = score
    score = score + 1
  return event_code_to_order_score

male_event_code_to_order_score = init_event_to_order_score(male_event_order)
female_event_code_to_order_score = init_event_to_order_score(female_event_order)

def entry_score(entry):
  #print(entry.event.short_name())
  if entry.is_male:
    return male_event_code_to_order_score[entry.event.event_code]
  return female_event_code_to_order_score[entry.event.event_code]

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
  if best_time is None:
    return None
  return RaceTime(best_time)

class RaceEntry():
  def __init__(self, swimmer, csv_entry):
    # Parse the event name string
    self.event = Event.create_from_long_event_str(csv_entry['Event'], course_code)
    self.time = RaceTime(csv_entry['Entry-Time'])
    self.pb = find_pb(self.event, swimmer.swims)
    self.comment = csv_entry['Comment']
    self.is_male = swimmer.is_male
    if self.comment == '""':
      self.comment = ''

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
  if asa_number not in asa_number_to_swimmer:
    print('Unknown swimmer: {name}'.format(name = entry['Name']))
    swimmer = Swimmer.from_swimming_events_csv(entry)
    print(swimmer.full_name())
    asa_number_to_swimmer[asa_number] = swimmer
  else:
    swimmer = asa_number_to_swimmer[asa_number]
  entering_swimmer = entering_swimmers.get(asa_number)
  if entering_swimmer is None:
    entering_swimmer = EnteringSwimmer(swimmer)
    entering_swimmers[asa_number] = entering_swimmer
  entering_swimmer.entries.append(RaceEntry(swimmer, entry))

def swimmer_sort_key(entering_swimmer):
  key = ""
  if entering_swimmer.swimmer.is_male:
    key = "M"
  else:
    key = "F"
  key = key + ' ' + entering_swimmer.swimmer.last_name + ' ' + entering_swimmer.swimmer.first_name
  return key

sorted_entering_swimmers = []
for asa_number, entering_swimmer in entering_swimmers.items():
  sorted_entering_swimmers.append(entering_swimmer)
sorted_entering_swimmers.sort(key = swimmer_sort_key)

# Output the data in a friendly fashion
print('\n\n---------------------------')
print('Swimmers:')
print('---------------------------')
for entering_swimmer in sorted_entering_swimmers:
  swimmer = entering_swimmer.swimmer
  print('{name}\n\tSwim England #: {asa_number}\n\tDate of Birth: {dob}'.format(name = swimmer.full_name(), asa_number = swimmer.asa_number, dob = swimmer.date_of_birth_str()))

print('\n\n---------------------------')
print('Events:')
print('---------------------------')
for entering_swimmer in sorted_entering_swimmers:
  swimmer = entering_swimmer.swimmer
  print('{name}'.format(name = swimmer.full_name()))

  entering_swimmer.entries.sort(key=entry_score)
  for entry in entering_swimmer.entries:
    pb_str = '-'
    if entry.pb is not None:
      pb_str = str(entry.pb)
    time = entry.pb
    #time = entry.time
    caution = False
    has_pb = False
    if entry.pb is not None:
      has_pb = True
      if float(entry.time) < (float(entry.pb) - 0.1):
        # Entry time is a lot faster than the actual PB
        # What gives?
        caution = True
      elif float(entry.time) < float(entry.pb):
        # Within 0.1s, so let's assume the entry time was rounded slightly aggressively and go with that
        time = entry.time
        pass

    if caution:
      print(f'\t{entry.event.short_name_without_course():<10} - Entry-Time:    {str(entry.time)+",":<10} PB: {pb_str+",":<10} Comment: "{entry.comment}"')
    elif not has_pb:
      print(f'\t{entry.event.short_name_without_course():<10} - Entry-Time:    {str(entry.time)+",":<10} PB: {"No PB,"  :<10} Comment: "{entry.comment}"')
    else:
      print(f'\t{entry.event.short_name_without_course():<10} - Official-Time: {str(entry.time)+",":<10}                Comment: "{entry.comment}"')
