import os

from swimmer import Swimmer
from swim import Swim
from event import Event

def parse_event(tokens, course_code):
  str = tokens[0][12:] # Because they all start with 'Male/Female'
  return Event.create_from_str( str, course_code )

def is_date(str):
  tokens = str.split('/')
  return len(tokens) == 3

def line_is_swimmer(tokens):
  return (len(tokens) == 4) and (tokens[3].strip().isdigit())

def line_is_swim(tokens):
  num_tokens = len(tokens)
  return ((num_tokens == 6) and is_date(tokens[1])) or ((num_tokens == 5) and is_date(tokens[0]) and (tokens[3] != '/'))

def line_is_event_type(tokens):
  return (len(tokens) == 1) and tokens[0].startswith('Male/Female')

def line_is_course_code(tokens):
  return (len(tokens) == 1) and (tokens[0].strip().endswith('Course'))

def ReadClubRankingsFile(file_name, swimmers, swimmers_dict, exclude_swimmers):
  club_rankings_file = open( file_name, 'r' )
  is_male = True
  current_swimmer = None
  current_event = None
  course_code = ''
  num_new_swimmers = 0
  num_new_swims = 0
  print("Reading " + file_name)
  for line in club_rankings_file:
    tokens = line.split('\t')
    if line_is_course_code(tokens):
      new_course_code = 'S'
      if tokens[0].strip().endswith('Long Course'):
        new_course_code = 'L'
      if course_code != new_course_code:
        # Announce the new course code
        course_code = new_course_code
        if course_code == 'S':
          print("Short Course")
        else:
          print("Long Course")
    elif line_is_swimmer(tokens):
      new_swimmer = Swimmer.from_club_rankings(is_male, tokens)
      if current_swimmer is not None:
        if is_male and (new_swimmer.last_name < current_swimmer.last_name):
          # Club rankings report has all the male swimmers followed by all the female swimmers
          #print("Switching from male to female")
          is_male = False
          new_swimmer.is_male = False
      if exclude_swimmers is not None and new_swimmer.full_name() in exclude_swimmers:
        # Effectively throw this swimmer away
        current_swimmer = new_swimmer
        new_swimmer = None
      elif new_swimmer.asa_number in swimmers_dict:
        # We've already seen this swimmer
        #if (current_swimmer is not None) and (current_swimmer.asa_number != new_swimmer.asa_number):
          #print("Continue " + str(new_swimmer))
        current_swimmer = swimmers_dict[new_swimmer.asa_number]
        new_swimmer = None
      if new_swimmer is not None:
        current_swimmer = new_swimmer
        swimmers_dict[current_swimmer.asa_number] = current_swimmer
        #print(str(current_swimmer))
        num_new_swimmers = num_new_swimmers + 1
        swimmers.append(current_swimmer)
        current_event = None
    elif line_is_event_type(tokens):
      assert(course_code != '')
      assert(current_swimmer is not None)
      current_event = parse_event(tokens, course_code)
      #print(str(current_event))
    elif line_is_swim(tokens):
      assert(current_swimmer is not None)
      assert(current_event is not None)
      swim = Swim(current_swimmer.asa_number, current_event, tokens)
      current_swimmer.swims.append(swim)
      num_new_swims = num_new_swims + 1
  print(str(num_new_swimmers) + " new swimmers and " + str(num_new_swims) + " new swims")

def ReadClubRankingsFiles(exclude_swimmers = None):
  swimmers = []
  swimmers_dict = {} # ASA number to swimmer
  
  for file in os.listdir("data"):
    if file.endswith(".txt"):
      ReadClubRankingsFile(os.path.join("data", file), swimmers, swimmers_dict, exclude_swimmers)
  swimmers.sort(key=Swimmer.sortBySurname)
  return swimmers