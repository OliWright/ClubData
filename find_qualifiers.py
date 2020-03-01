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
sys.path.append("qualifying_times")

import helpers
from swim import Swim
from swimmer import Swimmer
from race_time import RaceTime

from qualifying_event_wrapper import *

from event import short_course_events
from qualifying_times import get_qualifying_time
import read_club_rankings

folder = 'output/'
qt_file = open( folder + 'Qualifiers.txt', 'w' )
qt_html_file = open( folder + 'Qualifiers.html', 'w' )
maximum_age = 23 # Any swimmer older will be excluded

# Swimmers that are in our database that no longer swim for Winsford
excluded_swimmers = {
"Abbie Christopherson",
"Alice Deeming",
"Alisha Hawkins",
"Amber Rose",
"Anna Crossland",
"Ashley Hogg",
"Benjamin Townsend",
"Brandon Sharkey",
"Callum Chapple",
"Charlotte Howman",
"Charlotte Pagett",
"Daniel Hulme",
"Ellie Cushen",
"Emily Riddick",
"Georgia Farr",
"Grace Farr",
"Hannah McEnaney",
"Harrison Aspinall",
"Jamie Young",
"Jordan Gaskell",
"Kate Kenworthy",
"Kate Young",
"Katie Wilson",
"Keaton Haydon",
"Kyle Hawkins",
"Liadan Wilkes",
"Lily Harwood",
"Lydia Rose",
"Poppy Maskill",
"Rebecca Broadhurst",
"Rose Maskill",
"Samuel James",
"Thomas Bloor",
"William James"
}

age_on_date = helpers.ParseDate_dmY( age_on_date_str )
earliest_pb_date = helpers.ParseDate_dmY( earliest_pb_date_str )
num_events = len( short_course_events )
    
def process_swimmer( swimmer, swims ):
  age = helpers.CalcAge( swimmer.date_of_birth, age_on_date )
 
  full_name = swimmer.full_name()
  if full_name in excluded_swimmers:
    return;

  if age > maximum_age:
    return
  
  full_name = swimmer.alternate_name()
  # Find PB in the qualifying window, and qualifying PB
  pb_by_event = []
  qual_pb_by_event = []
  print( full_name )
  for i in range( 0, num_events ):
    pb_by_event.append( None )
    qual_pb_by_event.append( None )
  for swim in swims:
    if swim.date >= earliest_pb_date:
      event_code = swim.event.get_short_course_event_code()
      swim.converted_time = swim.race_time
      swim.is_converted = False
      swim.qualifies = (swim.level <= max_qualifying_meet_level)
      if swim.event.is_long_course() != is_long_course:
        swim.converted_time = swim.event.convert_time( swim.race_time )
        swim.is_converted = True
        #print( swim.event.short_name_without_course() + "\t" + str( swim.event.to_int() ) + "\t" + str( RaceTime( swim.race_time ) ) + "\t" + str( RaceTime( swim.converted_time ) ) + "\t" + swim.meet )
        # Round to 0.1s
        swim.converted_time = math.floor((swim.converted_time * 10) + 0.5) * 0.1

      qt = get_qualifying_time( event_code, swimmer.is_male, age )
      if (qt is None) or (swim.converted_time > qt):
        swim.qualifies = False

      if swim.qualifies:
        qual_pb = qual_pb_by_event[ event_code ]
        #print( "Considering: " + swim.event.short_name_without_course() + "\t" + str( swim.event.to_int() ) + "\t" + str( RaceTime( swim.race_time ) ) + "\t" + str( RaceTime( swim.converted_time ) ) + "\t" + swim.meet )
        if prefer_qualifying_times_in_target_course and (qual_pb is not None):
          # This meet insists that if you have qualifying times in the target course
          # then they should take precedence over other swims
          if qual_pb.is_converted and (not swim.is_converted):
            # Pretend the current qual_pb does not exist
            qual_pb = None
        if ((qual_pb is None) or (swim.converted_time < qual_pb.converted_time)):
          use_this_swim = True
          if prefer_qualifying_times_in_target_course and (qual_pb is not None):
            # This meet insists that if you have qualifying times in the target course
            # then they should take precedence over other swims
            if (not qual_pb.is_converted) and swim.is_converted:
              # Which means we can't use this swim
              use_this_swim = False
          if use_this_swim:
            qual_pb_by_event[ event_code ] = swim

      pb = pb_by_event[ event_code ]
      if (pb is None) or (swim.converted_time < pb.converted_time):
        #print( "PB: " + swim.event.short_name_without_course() + "\t" + str( swim.event.to_int() ) + "\t" + str( RaceTime( swim.race_time ) ) + "\t" + str( RaceTime( swim.converted_time ) ) + "\t" + swim.meet )
        pb_by_event[ event_code ] = swim

  printed_name = False
  converted_from_course_name = "LC"
  if is_long_course:
    converted_from_course_name = "SC"

  for i in range( 0, num_events ):
    qt = get_qualifying_time( i, swimmer.is_male, age )
    if qt is not None:
      pb = qual_pb_by_event[i]
      if (pb is None) or (pb.converted_time > qt):
        # There isn't a time from a qualifying event, or it was too slow.
        # Let's consider a non-qualifying event instead (if there is one).
        #if pb is not None:
        #  print( "Slow: " + str(i) + ", " + str( pb.converted_time ) + ", " + str( qt ) )
        pb = pb_by_event[i]
      if pb is not None:
        race_time = pb.converted_time
        if race_time <= qt:
          tag_class = "qualified"
          if not pb.qualifies:
            tag_class = "not-qualified"
          if not printed_name:
            qt_file.write( full_name + " (" + str(age) + ")\n" )
            qt_html_file.write( '<tr class="name"><th colspan="5">' + full_name + " (" + str(age) + ")</th></tr>\n" )
            printed_name = True
          precision = 2
          conversion_str = ""
          if pb.is_converted:
            precision = 1
            conversion_str = '<small> (' + str( RaceTime( pb.race_time ) ) + ' ' + converted_from_course_name + ')</small>'
          qt_file.write( "\t" + pb.event.short_name_without_course() + "\t" + str( RaceTime( race_time, precision ) ) + "\t" + pb.meet + "\t" + pb.date.strftime( '%d/%m/%Y' ) + "\n" )
          qt_html_file.write( '<tr class="' + tag_class + '"><td> </td><td>' + pb.event.short_name_without_course() + "</td><td>" + str( RaceTime( race_time, precision ) ) + "</td><td>" + pb.meet + "</td><td>" + pb.date.strftime( '%d/%m/%Y' ) + "</td></tr>\n" )
  if printed_name:
    qt_file.write( "\n" )

qt_html_file.write( '<table>' )    

# Read the swim list and process the swimmers
swimmers = read_club_rankings.ReadClubRankingsFiles()
swimmers.sort(key=Swimmer.sortBySurname)
for swimmer in swimmers:
  if True: #swimmer.full_name() == "Sophie George":
    process_swimmer(swimmer, swimmer.swims)

qt_file.close()    

qt_html_file.write( '</table>' )    
qt_html_file.close()    

