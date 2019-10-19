# Winsford ASC Club Champs Scoring System
#   qualifying_times.py
#   The times to use for calculating who qualifies for what
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
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import print_function

from event import Event
from event import short_course_events
from race_time import RaceTime

from qualifying_event_wrapper import *

def _parse_spreadsheet_data( spreadsheet_data ):
  rows = spreadsheet_data.split( '\n' )

  num_events = len( short_course_events )
  qt_by_event = [ None ] * num_events
  expected_num_columns = max_age - min_age + 2
  
  for row in rows:
    columns = row.split( '\t' )
    # Parse the event name
    event_code = Event.create_from_str( columns[0], 'S' ).event_code
    if len( columns ) != expected_num_columns:
      raise RuntimeError( "Unexpected number of columns in spreadsheet data" )
    qt_for_event = []
    qt_by_event[ event_code ] = qt_for_event
    for i in range( 1, expected_num_columns ):
      if len( columns[i] ) == 0:
        qt_for_event.append( None )
      else:
        qt_for_event.append( float( RaceTime( columns[i] ) ) )
  return qt_by_event
        
_boys_qt_by_event = _parse_spreadsheet_data( BOYS_SPREADSHEET_DATA_STR )
_girls_qt_by_event = _parse_spreadsheet_data( GIRLS_SPREADSHEET_DATA_STR )
    
def get_qualifying_time( event_code, is_male, age ):
  qt_for_event = None
  if is_male:
    qt_for_event = _boys_qt_by_event[ event_code ]
  else:
    qt_for_event = _girls_qt_by_event[ event_code ]
  if qt_for_event is None:
    return None
  qt_age = age
  if age < min_age:
    qt_age = min_age
  if age > max_age:
    qt_age = max_age
  # Add a very small epsilon, because it looks like our roundings
  # still have very small errors which can make <= testing fail
  # on numbers that superficially appear very equal.
  return qt_for_event[ qt_age - min_age ] + 0.000000001

  
def _print_qualifying_times( qt_by_event, heading, do_conversion ):
  print('<table><tbody><tr class="' + heading.lower() + '"><th>' + heading + '</th>')
  for age in range(min_age, max_age+1):
    print('<th>' +str(age) + '</th>')
  print('</tr>')
  course_code = "S"
  if is_long_course:
    course_code = "L"
  num_events = len( short_course_events )
  precision = 2
  if do_conversion:
    precision = 1
  for event_code in range(num_events):
    times = qt_by_event[ event_code ]
    if times is not None:
      event = Event.create_from_code(event_code, course_code)
      print('<tr class="' + event.short_stroke_name().lower() + '"><td>' + event.short_name_without_course() + '</td>')
      for time in times:
        converted_time = time
        if do_conversion:
          converted_time = event.convert_time(time)
        print('<td>'+ str(RaceTime(converted_time, precision=precision)) + '</td>')
      print('</tr>')
  print('</tbody></table>')
  
def convert_qualifying_times():
  if(is_long_course):
    print('<h3>Long Course Times</h3>')
  else:
    print('<h3>Short Course Times</h3>')
  _print_qualifying_times(_boys_qt_by_event, "Boys", False)
  _print_qualifying_times(_girls_qt_by_event, "Girls", False)
  if(is_long_course):
    print('<h3>Short Course Times</h3>')
  else:
    print('<h3>Long Course Times</h3>')
  _print_qualifying_times(_boys_qt_by_event, "Boys", True)
  _print_qualifying_times(_girls_qt_by_event, "Girls", True)
