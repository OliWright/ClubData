# Winsford ASC Google AppEngine App
#   find_qualifiers.py
#   Reads a text file containing all swims for all swimmers in the club
#   and figures out who qualifies for the events listed in qualifying_times.py
#
# Copyright (C) 2014 Oliver Wright
#    oli.wright.github@gmail.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program (file LICENSE); if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.import logging

import logging
import time
import datetime
import re
import math

from operator import attrgetter

import sys
sys.path.append("modules")

import helpers
from swim import Swim
from swimmer import Swimmer
from race_time import RaceTime

from event import short_course_events
import read_club_rankings

folder = 'output/'
records_html_file = open( folder + 'Records.html', 'w' )

num_events = len( short_course_events )

min_age = 9
open_age = 18

m_sc_records_by_age = []
m_lc_records_by_age = []
f_sc_records_by_age = []
f_lc_records_by_age = []
for age in range(min_age, open_age + 1):
  m_sc_records_by_age.append([ None ] * num_events)
  m_lc_records_by_age.append([ None ] * num_events)
  f_sc_records_by_age.append([ None ] * num_events)
  f_lc_records_by_age.append([ None ] * num_events)

asa_number_to_swimmer = {}

def process_swimmer( swimmer, swims ):
  full_name = swimmer.alternate_name()
  asa_number_to_swimmer[swimmer.asa_number] = swimmer
  for swim in swims:
    age_on_date = helpers.CalcAge( swimmer.date_of_birth, swim.date )
    if age_on_date < min_age:
      age_on_date = min_age
    if age_on_date > open_age:
      age_on_date = open_age
    if swimmer.is_male:
      if swim.event.is_long_course():
        records_for_age_by_event = m_lc_records_by_age[age_on_date - min_age]
      else:
        records_for_age_by_event = m_sc_records_by_age[age_on_date - min_age]
    else:
      if swim.event.is_long_course():
        records_for_age_by_event = f_lc_records_by_age[age_on_date - min_age]
      else:
        records_for_age_by_event = f_sc_records_by_age[age_on_date - min_age]
    record = records_for_age_by_event[swim.event.get_short_course_event_code()]
    if record is None or swim.race_time < record.race_time:
      records_for_age_by_event[swim.event.get_short_course_event_code()] = swim

# Read the swim list and process the swimmers
swimmers = read_club_rankings.ReadClubRankingsFiles()
for swimmer in swimmers:
  if True: #swimmer.full_name() == "Sophie George":
    process_swimmer(swimmer, swimmer.swims)

def write_records_for_age(age, records_by_event):
  print('Age: {0}'.format(age))
  for event_code in range(num_events):
    swim = records_by_event[event_code];
    if swim is not None:
      swimmer = asa_number_to_swimmer[swim.asa_number]
      print('{0}: {1}: {2}'.format(swim.event.short_name_without_course(), swimmer.alternate_name(), str( RaceTime( swim.race_time ) )))

def write_records(records_by_age):
  for age in range(min_age, open_age + 1):
    write_records_for_age(age, records_by_age[age - min_age])

records_html_file.write( '<table>' )

print('Girls Short Course')
write_records(f_sc_records_by_age)
print('Girls Long Course')
write_records(f_lc_records_by_age)
print('Boys Short Course')
write_records(m_sc_records_by_age)
print('Boys Long Course')
write_records(m_lc_records_by_age)

records_html_file.write( '</table>' )
records_html_file.close()

