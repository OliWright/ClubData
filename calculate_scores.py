# Winsford ASC Google AppEngine App
#	 make_consideration_times.py
#	 Reads a text file containing all swims for all swimmers in the club
#	 and figures out a scoring consideration time for each swimmer for each
#	 event based on their PB, or an interpolated PB from a year before
#	 the date of the club champs.
#
# Copyright (C) 2014 Oliver Wright
#		oli.wright.github@gmail.com
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program (file LICENSE); if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.import logging

import logging
import time
import datetime
import helpers
import re
import math

from operator import attrgetter

import sys
sys.path.append("modules")
sys.path.append("qualifying_times")

from swim import Swim
from swimmer import Swimmer
from race_time import RaceTime
from event import Event

from event import short_course_events
from nt_consideration_times import get_nt_consideration_time

_SPREADSHEET_DATA_STR = """50 Free	0.3	0.26	0.22	0.2	0.18	0.17	0.16	0.15
100 Free	0.75	0.65	0.55	0.5	0.45	0.425	0.4	0.375
200 Free	1.5	1.3	1.1	1	0.9	0.85	0.8	0.75
400 Free	3.75	3.25	2.75	2.5	2.25	2.125	2	1.875
800 Free	6	5.2	4.4	4	3.6	3.4	3.2	3
1500 Free	12	10.4	8.8	8	7.2	6.8	6.4	6
50 Breast	0.45	0.39	0.33	0.3	0.27	0.255	0.24	0.225
100 Breast	1.125	0.975	0.825	0.75	0.675	0.6375	0.6	0.5625
200 Breast	2.25	1.95	1.65	1.5	1.35	1.275	1.2	1.125
50 Fly	0.345	0.299	0.253	0.23	0.207	0.1955	0.184	0.1725
100 Fly	0.8625	0.7475	0.6325	0.575	0.5175	0.48875	0.46	0.43125
200 Fly	1.725	1.495	1.265	1.15	1.035	0.9775	0.92	0.8625
50 Back	0.36	0.312	0.264	0.24	0.216	0.204	0.192	0.18
100 Back	0.9	0.78	0.66	0.6	0.54	0.51	0.48	0.45
200 Back	1.8	1.56	1.32	1.2	1.08	1.02	0.96	0.9
100 IM	0.975	0.845	0.715	0.65	0.585	0.5525	0.52	0.4875
200 IM	1.8	1.56	1.32	1.2	1.08	1.02	0.96	0.9
400 IM	4.5	3.9	3.3	3	2.7	2.55	2.4	2.25"""

folder = 'f:/SwimLists/'
consideration_times_file = open( folder + 'ConsiderationTimes.txt', 'r' )
race_times_file = open( folder + 'RaceTimes.txt', 'r' )
missing_consideration_times_file = open( folder + 'MissingConsiderationTimes.txt', 'w' )
club_champs_date_str = '21/9/2019'

club_champs_date = helpers.ParseDate_dmY( club_champs_date_str )
num_events = len( short_course_events )

def _parse_spreadsheet_data( spreadsheet_data ):
	rows = spreadsheet_data.split( '\n' )

	num_events = len( short_course_events )
	seconds_per_point_by_event = [ None ] * num_events
	
	for row in rows:
		columns = row.split( '\t' )
		# Parse the event name
		event_code = Event.create_from_str( columns[0], 'S' ).event_code
		if len( columns ) != 9:
			raise RuntimeError( "Unexpected number of columns in spreadsheet data" )
		seconds_per_point_for_event = []
		seconds_per_point_by_event[ event_code ] = seconds_per_point_for_event
		for i in range( 1, 9 ):
			if len( columns[i] ) == 0:
				seconds_per_point_for_event.append( None )
			else:
				seconds_per_point_for_event.append( float( columns[i] ) )
	return seconds_per_point_by_event
				
seconds_per_point_by_event = _parse_spreadsheet_data( _SPREADSHEET_DATA_STR )

class EventCodeAndTime():
	def __init__(self, line):
		tokens = line.split( "|" )
		num_tokens = len( tokens )
		assert( (num_tokens == 2) or (num_tokens == 3) )
		
		self.event_code = Event.create_from_str( tokens[0], "S" ).get_short_course_event_code()
		self.time = float( RaceTime( tokens[1] ) )
		if num_tokens == 3:
			self.is_nt = (tokens[2] == 'nt\n')
		else:
			self.is_nt = False

class RaceConsideration():
	def __init__(self, event_code, consideration_time, race_time, consideration_is_nt ):
		self.event = short_course_events[ event_code ]
		self.consideration_time = consideration_time
		self.time = race_time
		self.consideration_is_nt = consideration_is_nt
		
class SwimmerTimes():
	def __init__(self, swimmer, full_name):
		self.swimmer = swimmer
		self.full_name = full_name
		self.race_by_event = []
		self.age = helpers.CalcAge( swimmer.date_of_birth, club_champs_date )

		for i in range( 0, num_events ):
			self.race_by_event.append( None )

swimmer_times_by_name = {}
unmatched_swimmer_names = []
		
def process_swimmer( swimmer, races ):
	global swimmer_times_by_name
	global unmatched_swimmer_names
	full_name = swimmer.full_name()
	swimmer_times = SwimmerTimes( swimmer, full_name )
	swimmer_times_by_name[ full_name ] = swimmer_times
	
	# Categorise swims by event
	for race in races:
		swimmer_times.race_by_event[ race.event_code ] = RaceConsideration( race.event_code, race.time, None, race.is_nt )
 
	print( full_name )

def add_races_for_swimmer( swimmer, races ):
	global swimmer_times_by_name
	global unmatched_swimmer_names
	full_name = swimmer.full_name()
	if full_name not in swimmer_times_by_name:
		unmatched_swimmer_names.append( full_name )
		return
	
	swimmer_times = swimmer_times_by_name[ full_name ]
	for race in races:
		if swimmer_times.race_by_event[ race.event_code ] is None:
			swimmer_times.race_by_event[ race.event_code ] = RaceConsideration( race.event_code, None, race.time, True )
		else:
			swimmer_times.race_by_event[ race.event_code ].time = race.time
 
	print( full_name )
		
# Read the consideration times list
reading_swims = False
swimmer = None
races = []
for line in consideration_times_file:
	if reading_swims:
		if len( line ) <= 1:
			# Empty line.	So we've finished reading all the swims for a swimmer
			reading_swims = False
			process_swimmer( swimmer, races )
			races = []
		else:
			# Expect the line to be a Swim
			race = EventCodeAndTime( line )
			races.append( race )
	else:
		# Expect the line to be a Swimmer
		swimmer = Swimmer.from_old_format( line )
		reading_swims = True

# We've read the entire file.
if reading_swims:
	# We won't have processed the final swimmer...
	reading_swims = False
	process_swimmer( swimmer, races )
	races = []

# Read the race times
for line in race_times_file:
	if reading_swims:
		if len( line ) <= 1:
			# Empty line.	So we've finished reading all the swims for a swimmer
			reading_swims = False
			add_races_for_swimmer( swimmer, races )
			races = []
		else:
			# Expect the line to be a Swim
			race = EventCodeAndTime( line )
			races.append( race )
	else:
		# Expect the line to be a Swimmer
		swimmer = Swimmer.from_old_format( line )
		reading_swims = True

# We've read the entire file.
if reading_swims:
	# We won't have processed the final swimmer...
	reading_swims = False
	add_races_for_swimmer( swimmer, races )
	races = []

sorted_scores_boys = []
sorted_scores_girls = []
	
# Do the scoring
for name, swimmer_times in swimmer_times_by_name.items():
	swimmer = swimmer_times.swimmer
	total_points = 0
	age_for_points = swimmer_times.age
	print( swimmer.full_name() + " " + str(age_for_points) )
	if age_for_points > 16:
		age_for_points = 16
	age_column = age_for_points - 9
	for race in swimmer_times.race_by_event:
		if race is not None:
			race.points = 0
			if (race.time is not None) and (race.consideration_time) is not None:
				improvement = race.consideration_time - race.time
				event_code = race.event.get_short_course_event_code()
				points = improvement / seconds_per_point_by_event[ event_code ][ age_column ]
				print( str(race.event) + " " + str(seconds_per_point_by_event[ event_code ][ age_column ]) + " " + str(improvement) )
				points = int( math.ceil( points - 0.00001 ) )
				max_points = 10
				if race.consideration_is_nt:
					max_points = 5
				if points < 0:
					points = 0
				elif points > max_points:
					points = max_points
				race.points = points
				total_points += points
	swimmer_times.points = total_points
	if swimmer.is_male:
		sorted_scores_boys.append( swimmer_times )
	else:
		sorted_scores_girls.append( swimmer_times )
sorted_scores_boys.sort( key=attrgetter('points'), reverse=True )
sorted_scores_girls.sort( key=attrgetter('points'), reverse=True )

# Now we produce the output files
def write_scores( sorted_scores, file_name ):
	print( 'Writing file' )
	scores_file = open( folder + file_name, 'w' )
	number = 1
	for swimmer_times in sorted_scores:
		swimmer = swimmer_times.swimmer
		age_for_points = swimmer_times.age
		if age_for_points > 16:
			age_for_points = 16
		age_column = age_for_points - 9
		scores_file.write( '<p class="question">' )
		scores_file.write( str(number) + ': ' + swimmer_times.full_name + ' (' + str( swimmer_times.points ) + ' points)' )
		scores_file.write( '</p>\n' )
		scores_file.write( '<div class="answer"><table><tr><th>Event</th><th>Consideration Time</th><th>Race Time</th><th>Points</th></tr>\n' )
		for race in swimmer_times.race_by_event:
			if (race is not None) and (race.time is not None):
				scores_file.write( '<tr><td>' + race.event.short_name_without_course() + '</td>' )
				if race.consideration_time is not None:
					nt_str = ''
					if race.consideration_is_nt:
						nt_str = '(NT) '
					scores_file.write( '<td>' + nt_str + str( RaceTime( race.consideration_time ) ) + '</td>' )
				else:
					scores_file.write( '<td>Missing Consideration Time</td>' )
				scores_file.write( '<td>' + str( RaceTime( race.time ) ) + '</td>' )
				scores_file.write( '<td>' + str( race.points ) + '</td>' )
				scores_file.write( '</tr>\n' )
		scores_file.write( '</table></div>\n' )
		number = number + 1
	scores_file.close()		

write_scores( sorted_scores_boys, "ScoresBoys.html" )
write_scores( sorted_scores_girls, "ScoresGirls.html" )
	
# Write out the list of entries that we haven't processed any data for
for name in unmatched_swimmer_names:
	missing_consideration_times_file.write( name + '\n' )
missing_consideration_times_file.close()		
