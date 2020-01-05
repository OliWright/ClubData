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
import re

from operator import attrgetter

import sys
sys.path.append("modules")
sys.path.append("qualifying_times")

import helpers
from swim import Swim
from swimmer import Swimmer
from race_time import RaceTime

from event import short_course_events
from nt_consideration_times import get_nt_consideration_time

import read_club_rankings

folder = 'output/'
#entry_list_file = open( folder + 'EntryList.txt', 'r' )
consideration_times_file = open( folder + 'ConsiderationTimes.txt', 'w' )
consideration_times_verbose_file = open( folder + 'ConsiderationTimesVerbose.txt', 'w' )
consideration_times_html_index_file = open( folder + 'consideration_times_2019_index.html', 'w' )
club_champs_start_date_str = '8/9/2019'
club_champs_date_str = '21/9/2019'
maximum_age = 21 # Any swimmer older will be excluded
previous_club_champs_name = "Winsford Swim Team Club Championships"

club_champs_start_date = helpers.ParseDate_dmY( club_champs_start_date_str )
club_champs_date = helpers.ParseDate_dmY( club_champs_date_str )
consideration_date = datetime.date( club_champs_date.year - 1, club_champs_date.month, club_champs_date.day )
consideration_date_str = consideration_date.strftime( '%d/%m/%Y' )
num_events = len( short_course_events )

class ConsiderationTime():
	def __init__(self, event, time, reason, is_nt):
		self.event = event
		self.time = time
		self.reason = reason
		self.is_nt = is_nt

class SwimmerTimes():
	def __init__(self, swimmer, full_name):
		self.swimmer = swimmer
		self.full_name = full_name
		self.consideration_times = []

all_swimmer_times = []
entries = {}

def process_swimmer( swimmer, swims ):
	age = helpers.CalcAge( swimmer.date_of_birth, club_champs_date )
 
	full_name = swimmer.full_name()
	# if not full_name in entries:
		# full_name = swimmer.alternate_name()
		# if not full_name in entries:
			# print( 'Excluding ' + full_name + ', ' + str( age ) + '. Not in entry list.' )
			# return

	if age > maximum_age:
		print( 'Excluding ' + full_name + ', ' + str( age ) + '. Too old.' )
		return
	
	entries[ full_name ] = True
	
	# Categorise swims by event
	swims_by_event = []
	for i in range( 0, num_events ):
		swims_by_event.append( [] )
	for swim in swims:
		# Append to the list according to short course event code
		swims_by_event[ swim.event.get_short_course_event_code() ].append( swim )
		
	# Sort the swims in each event by date
	for i in range( 0, num_events ):
		swims_by_event[i].sort( key=attrgetter('date') )

	swimmer_times = SwimmerTimes( swimmer, full_name )
	all_swimmer_times.append( swimmer_times )
	
	print( full_name + ', ' + str( age ) )
	for i in range( 0, num_events ):
		event = short_course_events[i]
		event_swims = swims_by_event[i]
		pb_swim = None
		interp_swim = None
		for swim in event_swims:
			if swim.short_course_race_time < 1.0:
				continue # Disregard because it's nonsense
			if swim.date >= club_champs_start_date:
				continue # Disregard this for any PB consideration
			if swim.meet == previous_club_champs_name:
				# This swim was at the previous club champs.
				# If it's a PB, then we just use that.
				if (pb_swim is None) or (swim.short_course_race_time < pb_swim.short_course_race_time):
					pb_swim = swim
					break
			if swim.date <= consideration_date:
				# This swim is earlier than the consideration date.
				# Is it a PB?
				if (pb_swim is None) or (swim.short_course_race_time < pb_swim.short_course_race_time):
					pb_swim = swim
			else:
				if pb_swim is None:
					# There was no time set before the consideration date
					break
				else:
					if swim.short_course_race_time < pb_swim.short_course_race_time:
						# This is the first swim after the consideration date that's a PB.
						interp_swim = swim
						break
		consideration_time = None
		if pb_swim is None:
			nt_time = get_nt_consideration_time( i, swimmer.is_male, age )
			if nt_time is None:
				consideration_time = ConsiderationTime( event, None, 'No PB as of ' + consideration_date_str + ', and no time specified in the NT table', True )
			else:
				consideration_time = ConsiderationTime( event, nt_time, 'No PB as of ' + consideration_date_str + ', so consideration time taken from the NT table', True )
		else:
			if interp_swim is not None:
				# Interpolate the PB between the pre-consideration-date PB and the first PB
				# race after the consideration date
				interpolation_val = float( (consideration_date - pb_swim.date).days ) / float( (interp_swim.date - pb_swim.date).days )
				consideration_race_time = (interp_swim.short_course_race_time * interpolation_val) + (pb_swim.short_course_race_time * (1 - interpolation_val))
				consideration_time = ConsiderationTime( event, consideration_race_time, 'Interpolated between ' + pb_swim.meet + ' ' + pb_swim.date.strftime( "%d/%m/%Y" ) + ' (' + str( RaceTime( pb_swim.short_course_race_time ) ) + ') and ' + interp_swim.meet + ' ' + interp_swim.date.strftime( "%d/%m/%Y" )+ ' (' + str( RaceTime( interp_swim.short_course_race_time ) ) + ')', False )
			else:
				consideration_time = ConsiderationTime( event, pb_swim.short_course_race_time, 'From ' + pb_swim.meet + ' on ' + pb_swim.date.strftime( "%d/%m/%Y" ), False )
		swimmer_times.consideration_times.append( consideration_time )


# Read all the data from the club rankings exports
swimmers = read_club_rankings.ReadClubRankingsFiles()
for swimmer in swimmers:
  process_swimmer(swimmer, swimmer.swims)

# Now we produce the output files
print( 'Writing file' )
first = True
for swimmer_times in all_swimmer_times:
	if not first:
		consideration_times_file.write( '\n' )
	swimmer = swimmer_times.swimmer
	consideration_times_file.write( str( swimmer ) + '\n' )
	for consideration_time in swimmer_times.consideration_times:
		if consideration_time.time is not None:
			is_pb_str = 'pb'
			if consideration_time.is_nt:
				is_pb_str = 'nt'
			consideration_times_file.write( consideration_time.event.short_name_without_course() + '|' + str( RaceTime( consideration_time.time ) ) + '|' + is_pb_str + '\n' )
	first = False
consideration_times_file.close()		

first = True
for swimmer_times in all_swimmer_times:
	if not first:
		consideration_times_verbose_file.write( '\n' )
	swimmer = swimmer_times.swimmer
	age = helpers.CalcAge( swimmer.date_of_birth, club_champs_date )
	consideration_times_verbose_file.write( swimmer_times.full_name + ', ' + str( age ) + '\n' )
	for consideration_time in swimmer_times.consideration_times:
		if consideration_time.time is not None:
			consideration_times_verbose_file.write( '\n' + consideration_time.event.short_name_without_course() + ': ' + str( RaceTime( consideration_time.time ) ) + '\n' )
			consideration_times_verbose_file.write( consideration_time.reason + '\n' )
	first = False
consideration_times_verbose_file.close()

_HTML_TOP = ''
_HTML_DESCRIPTION = """<p>The scoring for Best Boy and Best Girl for the Club Champs will be done slightly differently this year. We want to encourage swimmers to improve themselves, so we're basing the scores on how much they've improved over the year.</p>
<p>To do this we take each swimmers' PB in each event from one year before the date of the Club Champs as a consideration time. Points are then awarded according to how much they improve on that time. The time needed for each point is set by the coaches, and varies with age and event. This is because a 10 year old might knock 20s off their 200 Breast time, whereas it's very difficult for a 16 year old to knock 1s off their 50 free time for example.</p>
<p>Consideration times are calculated by looking for PBs around 19/9/2014. We find their PB race before this date, then we find their first PB race after this date, then we interpolate to get a fair PB for 19/9/2014. This is to make it as fair as possible, to eliminate any effect of 'when' the PB was set.</p>
<p>Where there is no PB set after 19/9/2014, we take the PB before that date. Where there is no PB before that date, we take a consideration time from a table of times defined by the coaches, based on the North Mids qualifying times for 2014. In those cases, the swimmer will not be eligible for a maximum score tally because we're not able to measure an improvement.</p>
<p>Below is a list of links to each swimmer's consideration times and how they have been calculated.</p>
<p>There are some swimmers missing from this list. Possible causes are...</p>
<ul>
	<li>Swimmer is listed as Cat 1 on the <a href="https://www.swimmingresults.org/membershipcheck/">ASA database</a>.</li>
	<li>Swimmer has recently switched to Cat 2.</li>
	<li>Somebody pressed the wrong button.</li>
</ul>
<p>We will try to make sure that all swimmers get correct consideration times.	Swimmers that compete in the Club Champs but are not listed here, will be given consideration times by the coaches.</p>
<p>If you have any questions, or if a swimmer is not listed but <em>does</em> have PBs from before 19/9/2014, please contact <a href="mailto:ol.wright@gmail.com?Subject=Club%20Champs%20Scoring%20Query">Oli Wright</a>.</p>
"""

_HTML_BOTTOM = ''

consideration_times_html_index_file.write( _HTML_TOP )
#consideration_times_html_index_file.write( _HTML_DESCRIPTION )
consideration_times_html_index_file.write( '<ul>' )
for swimmer_times in all_swimmer_times:
	swimmer = swimmer_times.swimmer
	age = helpers.CalcAge( swimmer.date_of_birth, club_champs_date )
	
	html = '<li><a href="'
	page_name = 'individual_consideration_times_2019/' + str( swimmer.asa_number ) + '.html'
	html += page_name
	html += '">' + swimmer_times.full_name + '</a></li>'
	consideration_times_html_index_file.write( html + '\n' )
	
	consideration_times_html_file = open( folder + page_name, 'w' )
	consideration_times_html_file.write( _HTML_TOP )
	
	html = '<h2>' + swimmer_times.full_name + ', ' + str( age ) + '</h2>'
	consideration_times_html_file.write( html )
	for consideration_time in swimmer_times.consideration_times:
		if consideration_time.time is not None:
			html = '<h3>' + consideration_time.event.short_name_without_course() + ': ' + str( RaceTime( consideration_time.time ) ) + '</h3>'
			html += '<p>' + consideration_time.reason + '</p>'
			consideration_times_html_file.write( html )
			
	consideration_times_html_file.write( _HTML_BOTTOM )
	consideration_times_html_file.close()
	
consideration_times_html_index_file.write( '</ul>' )
consideration_times_html_index_file.write( _HTML_BOTTOM )
consideration_times_html_index_file.close()
