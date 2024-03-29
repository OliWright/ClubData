# Winsford ASC Club Champs Scoring System
#   event.py
#   Provides the Event class, which encapsulates a particular
#   swimming event (e.g. 50m FreeStyle Long Course)
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

import logging
import math

# This order matches the ASA 'stroke' code used in their swimming.org
# minus 1 (this array starts from 0)
strokeDistanceAndTurnFactors = (
(0, 50,   42.245),
(0, 100,  42.245),
(0, 200,  43.786),
(0, 400,  44.233),
(0, 800,  45.525),
(0, 1500, 46.221),
(1, 50,   63.616),
(1, 100,  63.616),
(1, 200,  66.598),
(2, 50,   38.269),
(2, 100,  38.269),
(2, 200,  39.76 ),
(3, 50,   40.5  ),
(3, 100,  40.5  ),
(3, 200,  41.98 ),
(4, 200,  49.7  ),
(4, 400,  55.366 ),
(4, 100,  45  )
)

stroke_id_to_string = ( "Freestyle", "Breaststroke", "Butterfly", "Backstroke", "IM" )
stroke_id_to_short_string = ( "Free", "Breast", "Fly", "Back", "IM" )
course_id_to_string = ( "Short", "Long" )
course_id_to_short_string = ( "SC", "LC" )

class Event:
  """Encapsulation of a swimming event type and course"""
  # Lower 8 bits is the ASA event code minus one
  # Bit 8 is 0 for short course, 1 for long course
  event_code = 0

  def __init__(self, event_code): 
    self.event_code = event_code

  @classmethod
  def create(cls, stroke_id, distance, course_code): 
    event_code = 0
    for stroke_id_and_distance in strokeDistanceAndTurnFactors:
      if (stroke_id_and_distance[0] == stroke_id) and (stroke_id_and_distance[1] == distance):
        break
      event_code = event_code + 1
    if course_code == "L":
      event_code = event_code | 0x100
    return cls( event_code )
  
  @classmethod
  def create_from_str( cls, string, course_code ):
    # Parse event of the form "50 Freestyle" from swimmingresults.org
    substrings = string.split()
    distance = int( substrings[0] )
    stroke_id = None
    if substrings[1].lower().startswith( 'fr' ):
      stroke_id = 0
    elif substrings[1].lower().startswith( 'br' ):
      stroke_id = 1
    elif substrings[1].lower().startswith( 'bu' ) or substrings[1].lower().startswith( 'fl' ):
      stroke_id = 2
    elif substrings[1].lower().startswith( 'ba' ):
      stroke_id = 3
    elif substrings[1].lower().startswith( 'i' ): # "Medley" would be in substrings[2]
      stroke_id = 4
    if stroke_id is None:
      return
    return cls.create( stroke_id, distance, course_code )
  
  @classmethod
  def create_from_long_event_str( cls, string, course_code):
    # More general parsing that can cope with the likes of
    # "Girls 10 Yrs/Over 100m Butterfly"
    distance = 50
    stroke_id = None
    substrings = string.split()
    for substring in substrings:
      if substring.lower().startswith( 'fr' ):
        stroke_id = 0
      elif substring.lower().startswith( 'br' ):
        stroke_id = 1
      elif substring.lower().startswith( 'bu' ) or substrings[1].lower().startswith( 'fl' ):
        stroke_id = 2
      elif substring.lower().startswith( 'ba' ):
        stroke_id = 3
      elif substring.lower().startswith( 'in' ) or substring.lower().startswith( 'im' ):
        stroke_id = 4
      elif substring.startswith( '50' ):
        distance = 50
      elif substring.startswith( '100' ):
        distance = 100
      elif substring.startswith( '200' ):
        distance = 200
      elif substring.startswith( '400' ):
        distance = 400
      elif substring.startswith( '800' ):
        distance = 800
      elif substring.startswith( '1500' ):
        distance = 1500
    return cls.create( stroke_id, distance, course_code )

  @classmethod
  def create_from_code( cls, event_code, course_code ):
    if course_code == "L":
      event_code = event_code | 0x100
    return cls( event_code )
  
  def to_asa_event_number(self):
    return (self.event_code & 0xff) + 1
    
  def get_short_course_event_code(self):
    return self.event_code & 0xff
    
  def to_asa_course_code(self):
    if self.event_code & 0x100:
      return "L"
    else:
      return "S"

  def __str__(self):
    strokeDistanceAndTurnFactor = strokeDistanceAndTurnFactors[self.event_code & 0xff]
    stroke_id = strokeDistanceAndTurnFactor[0]
    distance = strokeDistanceAndTurnFactor[1]
    return str( distance ) + " " + stroke_id_to_string[ stroke_id ] + " " + course_id_to_string[ (self.event_code & 0x100) >> 8 ] + " Course"

  def to_string(self):
    return str(self)
    
  def to_int(self):
    return self.event_code

  def short_name_without_course(self):
    strokeDistanceAndTurnFactor = strokeDistanceAndTurnFactors[self.event_code & 0xff]
    stroke_id = strokeDistanceAndTurnFactor[0]
    distance = strokeDistanceAndTurnFactor[1]
    return str( distance ) + " " + stroke_id_to_short_string[ stroke_id ]

  def short_name(self):
    return self.short_name_without_course() + " " + course_id_to_short_string[ self.event_code >> 8 ]

  def short_stroke_name(self):
    strokeDistanceAndTurnFactor = strokeDistanceAndTurnFactors[self.event_code & 0xff]
    stroke_id = strokeDistanceAndTurnFactor[0]
    return stroke_id_to_short_string[ stroke_id ]
    
  def key(self):
    return self.event_code + 1

  def convert_time( self, raceTime ):
    strokeDistanceAndTurnFactor = strokeDistanceAndTurnFactors[self.event_code & 0xff]
    distance = strokeDistanceAndTurnFactor[1]
    turnFactor = strokeDistanceAndTurnFactor[2]
    if self.event_code & 0x100:
      # Convert long course to short course
      turnVal = (distance * 0.01) * turnFactor / raceTime
      numExtraTurnSC = distance * 0.02
      return raceTime - (turnVal * numExtraTurnSC)
    else:
      # Convert short course to long course
      # y = x - d.d.tf/100.50.x
      # yx = x2 - d2.tf/5000
      # yx - x2 = -d2.tf/5000
      # x2 - yx - d2.tf/5000 = 0
      # From quadratic... x = (-b +- sqrt(b2 -4ac)) / 2a
      # a = 1,   b = -y (short course time),   c = -d2.tf/5000
      # b = -raceTime;
      # c = distance * distance * turnFactor * -0.0002;
      # A couple of other simplifications and negation cancellings yields...
      conversion = (raceTime + math.sqrt( (raceTime * raceTime) + (distance * distance * turnFactor * 0.0008) )) * 0.5;
      # print( "distance: " + str( distance ) + ", turnFactor: " + str( turnFactor ) + ", raceTime: " + str( raceTime ) + ", conversion: " + str( conversion ) )
      return conversion

  def getDistance(self):
    return strokeDistanceAndTurnFactors[self.event_code & 0xff][1]
    
  def is_long_course(self):
    if self.event_code & 0x100:
      return True
    else:
      return False
    
short_course_events = (
Event.create( 0, 50, "S" ),
Event.create( 0, 100, "S" ),
Event.create( 0, 200, "S" ),
Event.create( 0, 400, "S" ),
Event.create( 0, 800, "S" ),
Event.create( 0, 1500, "S" ),
Event.create( 1, 50, "S" ),
Event.create( 1, 100, "S" ),
Event.create( 1, 200, "S" ),
Event.create( 2, 50, "S" ),
Event.create( 2, 100, "S" ),
Event.create( 2, 200, "S" ),
Event.create( 3, 50, "S" ),
Event.create( 3, 100, "S" ),
Event.create( 3, 200, "S" ),
Event.create( 4, 200, "S" ),
Event.create( 4, 400, "S" ),
Event.create( 4, 100, "S" ),
)
    
long_course_events = (
Event.create( 0, 50, "L" ),
Event.create( 0, 100, "L" ),
Event.create( 0, 200, "L" ),
Event.create( 0, 400, "L" ),
Event.create( 0, 800, "L" ),
Event.create( 0, 1500, "L" ),
Event.create( 1, 50, "L" ),
Event.create( 1, 100, "L" ),
Event.create( 1, 200, "L" ),
Event.create( 2, 50, "L" ),
Event.create( 2, 100, "L" ),
Event.create( 2, 200, "L" ),
Event.create( 3, 50, "L" ),
Event.create( 3, 100, "L" ),
Event.create( 3, 200, "L" ),
Event.create( 4, 200, "L" ),
Event.create( 4, 400, "L" ),
Event.create( 4, 100, "L" ),
)

num_events = len(short_course_events)