# Winsford ASC Club Champs Scoring System
#   swim.py
#   Lightweight version of the GAE swim.py used for offline processing
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


# Google Python style guide http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
#
# Naming...
# module_name, package_name, ClassName
# method_name, ExceptionName, function_name,
# GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name,
# function_parameter_name, local_var_name
#
# Prefix an _ to indicate privateness

import logging
import time
import datetime
import helpers
from event import Event
from race_time import RaceTime
    
class Swim():
  def __init__(self, line):
    tokens = line.split( "|" )
    num_tokens = len( tokens )
    
    # Figure out what version data we have
    version = 0
    if tokens[0].startswith( "V" ):
      version = int( tokens[0][1:] )

    if version == 1:
      self.asa_number = int( tokens[1] )
      self.event = Event( int( tokens[2] ) )
      self.date = helpers.ParseDate_dmY( tokens[3] )
      self.meet = tokens[4]
      self.asa_swim_id = int( tokens[5] )
      # Splits are in tokens[6]
      self.splits = tokens[6]
      self.is_licensed = True
      if tokens[7] == 'n':
        self.is_licensed = False
      self.race_time = float( tokens[8] )
      
      self.short_course_race_time = self.race_time
      if self.event.is_long_course():
        self.short_course_race_time = self.event.convert_time( self.race_time )
        
      #print( str( self.short_course_race_time ) )
    else:
      raise RuntimeError( "Unhandled swim version" )

  # Constructor for club rankings line
  def __init__(self, asa_number, event, tokens):
    token_offset = 0
    if len(tokens) == 6:
      token_offset = 1
    self.asa_number = asa_number
    self.event = event
    self.date = helpers.ParseDate_dmY( tokens[token_offset] )
    self.meet = tokens[token_offset + 1].strip()
    self.asa_swim_id = 0
    self.splits = None
    self.level = int(tokens[token_offset + 3])
    self.race_time = float( RaceTime(tokens[token_offset + 4]) )
    
    self.short_course_race_time = self.race_time
    if self.event.is_long_course():
      self.short_course_race_time = self.event.convert_time( self.race_time )
  
      
  # Returns the asa number of the swimmer that this swim is for.
  def get_asa_swim_id(self):
    if self.asa_swim_id == -1:
      return None
    return self.asa_swim_id
