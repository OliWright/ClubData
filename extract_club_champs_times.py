# Winsford ASC Swim Data Scripts
#   extract_club_champs_times.py
#   This reads the exported data from club rankings, and extracts
#   data for all the club champs races, writing the data out into a
#   simple text file.
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
race_times_file = open( folder + 'RaceTimes.txt', 'w' )
club_champs_start_date_str = '11/9/2022'
club_champs_end_date_str = '24/9/2022'
maximum_age = 21 # Any swimmer older will be excluded
club_champs_meet_name = 'Winsford Club Championships 2022'

club_champs_start_date = helpers.ParseDate_dmY( club_champs_start_date_str )
club_champs_end_date = helpers.ParseDate_dmY( club_champs_end_date_str )
num_events = len( short_course_events )

class ConsiderationTime():
  def __init__(self, event, time, reason):
    self.event = event
    self.time = time
    self.reason = reason

class SwimmerTimes():
  def __init__(self, swimmer, full_name):
    self.swimmer = swimmer
    self.full_name = full_name
    self.consideration_times = []
    self.swim_by_event = []

all_swimmer_times = []
    
def process_swimmer( swimmer, swims ):
  age = helpers.CalcAge( swimmer.date_of_birth, club_champs_end_date )
 
  full_name = swimmer.full_name()

  if age > maximum_age:
    print( 'Excluding ' + full_name + ', ' + str( age ) + '. Too old.' )
    return
  
  has_entered = False
  
  # Categorise swims by event
  swim_by_event = []
  for i in range( 0, num_events ):
    swim_by_event.append( None )
  for swim in swims:
    # Append to the list according to short course event code
    if (swim.meet == club_champs_meet_name) and (swim.date >= club_champs_start_date) and( swim.date <= club_champs_end_date):
      # This is a club champs swim
      swim_by_event[ swim.event.get_short_course_event_code() ] = swim
      has_entered = True

  if has_entered:
    print( full_name + ', ' + str( age ) )
    swimmer_times = SwimmerTimes( swimmer, full_name )
    swimmer_times.swim_by_event = swim_by_event
    all_swimmer_times.append( swimmer_times )


# Read all the data from the club rankings exports
swimmers = read_club_rankings.ReadClubRankingsFiles()
for swimmer in swimmers:
  process_swimmer(swimmer, swimmer.swims)
  
# Now we produce the output file
print( 'Writing file' )
first = True
for swimmer_times in all_swimmer_times:
  if not first:
    race_times_file.write( '\n' )
  swimmer = swimmer_times.swimmer
  race_times_file.write( str( swimmer ) + '\n' )
  for swim in swimmer_times.swim_by_event:
    if swim is not None:
      race_times_file.write( swim.event.short_name_without_course() + '|' + str( RaceTime( swim.race_time ) ) + '\n' )
  first = False
race_times_file.close()    
