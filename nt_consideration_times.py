# Winsford ASC Club Champs Scoring System
#   nt_consideration_times.py
#   The times to use for scoring consideration when no PB is available
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

from event import Event
from event import short_course_events
from race_time import RaceTime

_BOYS_SPREADSHEET_DATA_STR = """50 Free	56.01	56.01	50.01	49.01	46.5	46.01	45.82	45.22
100 Free	1.33.00	1.33.00	1.33.00	1.33.00	1.29.31	1.27.07	1.25.58	1.24.48
200 Free	4.25.01	4.25.01	3.30.00	3.20.00	3.15.00	3.10.00	3.05.00	3.03.00
400 Free	6.45.00	6.45.00	6.45.00	6.40.00	6.30.00	6.21.00	6.14.00	6.10.00
800 Free	13.20.40	13.20.40	13.20.40	13.20.40	12.34.00	12.22.40	11.59.20	11.47.60
1500 Free	23.30.00	23.30.00	23.30.00	23.00.00	22.30.00	22.00.00	21.30.00	21.00.00
50 Breast	1.05.01	1.05.01	1.04.4	58.01	53.01	50.01	50.01	50.01
100 Breast	2.05.80	2.05.80	2.05.80	1.51.31	1.45.22	1.42.14	1.39.80	1.38.17
200 Breast	5.00.00	5.00.00	4.36.03	4.23.93	4.13.05	4.05.92	4.01.22	3.59.10
50 Fly	1.00.00	1.00.00	55.01	52.01	51.01	49.5	49.01	48.8
100 Fly	1.51.80	1.51.80	1.51.80	1.40.33	1.36.14	1.33.23	1.31.03	1.29.93
200 Fly	5.01.00	5.01.00	4.16.51	4.05.30	3.56.50	3.49.90	3.44.17	3.41.86
50 Back	1.00.5	1.00.5	55.4	55.01	51.5	50.01	49.01	49.01
100 Back	1.43.01	1.43.01	1.43.01	1.41.01	1.36.85	1.33.74	1.31.72	1.30.61
200 Back	4.32.01	4.32.01	4.11.20	4.01.63	3.53.17	3.47.10	3.42.73	3.40.69
100 IM	1.43.00	1.43.00	1.35.00	1.29.00	1.24.00	1.20.00	1.14.00	1.11.00
200 IM	4.40.00	4.40.00	4.14.02	4.04.94	3.56.69	3.49.94	3.45.77	3.43.56
400 IM	7.10.00	7.10.00	7.10.00	6.50.00	6.30.00	5.20.00	5.10.00	5.05.00"""

_GIRLS_SPREADSHEET_DATA_STR = """50 Free	50.01	50.01	49.9	49.5	49.01	48.48	48.07	47.83
100 Free	1.36.97	1.36.97	1.36.97	1.33.80	1.32.19	1.30.91	1.30.14	1.29.67
200 Free	3.55.01	3.55.01	3.54.43	3.47.63	3.43.12	3.41.15	3.39.06	3.38.21
400 Free	7.15.00	7.15.00	7.00.00	6.45.00	6.30.00	6.30.00	6.15.00	6.00.00
800 Free	14.30.0	14.30.0	13.10.00	12.30.00	11.50.00	11.30.00	11.10.00	10.50.00
1500 Free	26.29.20	26.29.20	26.29.20	26.29.20	24.56.40	24.21.60	23.46.80	23.29.40
50 Breast	1.00.01	1.00.01	57.5	57	56.5	55.8	55.01	54.5
100 Breast	1.58.00	1.58.00	1.55.95	1.51.27	1.48.12	1.45.66	1.45.01	1.44.78
200 Breast	4.37.00	4.37.00	4.34.04	4.24.15	4.17.42	4.13.38	4.11.97	4.11.02
50 Fly	54.5	54.5	52.5	52	51.5	51	50.5	50.01
100 Fly	1.46.10	1.46.10	1.45.07	1.41.32	1.38.90	1.36.91	1.36.43	1.36.07
200 Fly	4.25.00	4.25.00	4.15.45	4.07.	4.00.94	3.56.20	3.53.86	3.53.8
50 Back	55	55	52	51.9	51	50.8	50.5	50.2
100 Back	1.46.30	1.46.30	1.45.62	1.41.29	1.38.99	1.37.78	1.36.42	1.36.18
200 Back	4.12.00	4.12.00	4.09.22	4.02.24	3.58.01	3.54.55	3.51.96	3.50.93
100 IM	1.45.00	1.45.00	1.40.00	1.35.00	1.30.00	1.25.00	1.20.00	1.18.00
200 IM	4.15.00	4.15.00	4.12.65	4.05.09	4.01.37	3.57.72	3.55.72	3.55.34
400 IM	7.30.00	7.30.00	7.10.00	6.50.00	6.40.00	6.33.00	6.30.00	6.28.00"""

def _parse_spreadsheet_data( spreadsheet_data ):
  rows = spreadsheet_data.split( '\n' )

  num_events = len( short_course_events )
  nt_times_by_event = [ None ] * num_events
  
  for row in rows:
    columns = row.split( '\t' )
    # Parse the event name
    event_code = Event.create_from_str( columns[0], 'S' ).event_code
    if len( columns ) != 9:
      raise RuntimeError( "Unexpected number of columns in spreadsheet data" )
    nt_times_for_event = []
    nt_times_by_event[ event_code ] = nt_times_for_event
    for i in range( 1, 9 ):
      if len( columns[i] ) == 0:
        nt_times_for_event.append( None )
      else:
        nt_times_for_event.append( float( RaceTime( columns[i] ) ) )
  return nt_times_by_event
        
_boys_nt_consideration_times_by_event = _parse_spreadsheet_data( _BOYS_SPREADSHEET_DATA_STR )
_girls_nt_consideration_times_by_event = _parse_spreadsheet_data( _GIRLS_SPREADSHEET_DATA_STR )
    
def get_nt_consideration_time( event_code, is_male, age ):
  nt_times_for_event = None
  if is_male:
    nt_times_for_event = _boys_nt_consideration_times_by_event[ event_code ]
  else:
    nt_times_for_event = _girls_nt_consideration_times_by_event[ event_code ]
  if nt_times_for_event is None:
    return None
  if age < 9:
    return None
  if age > 16:
    age = 16
  return nt_times_for_event[ age - 9 ]