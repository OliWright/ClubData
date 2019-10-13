# Winsford ASC Club Champs Scoring System
#   swimmer.py
#   Lightweight version of the GAE swimmer model used for off-line processing
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

import datetime
import helpers

class Swimmer():
  # Constructor
  def __init__(self, is_male, first_name, last_name, asa_number, date_of_birth, known_as = ''):
    self.is_male = is_male
    self.asa_number = asa_number
    self.last_name = last_name
    self.first_name = first_name
    self.known_as = known_as
    self.date_of_birth = date_of_birth
    self.swims = []
   
  
  # Constructor.  Passed in a row of text describing the swimmer.
  @classmethod
  def from_old_format(cls, str) -> 'Swimmer':
    tokens = str.split( '|' )
    num_tokens = len( tokens )
    is_male = False
    if tokens[4] == 'M':
      is_male = True
    asa_number = int(tokens[0])
    last_name = tokens[1]
    first_name = tokens[2]
    known_as = tokens[3]
    date_of_birth = helpers.ParseDate_dmY( tokens[5] )
    return cls(is_male, first_name, last_name, asa_number, date_of_birth, known_as)

  # Constructor for club rankings line
  @classmethod
  def from_club_rankings(cls, is_male, tokens) -> 'Swimmer':
    asa_number = int( tokens[3] )
    names = tokens[0].split(' ')
    last_name = names[1].strip()
    first_name = names[0].strip()
    known_as = ''
    date_of_birth = helpers.ParseDate_dmY( tokens[1] )
    return cls(is_male, first_name, last_name, asa_number, date_of_birth, known_as)

  def full_name(self):
    return self.first_name + " " + self.last_name

  def alternate_name(self):
    if self.known_as != '':
      return self.known_as + " " + self.last_name
    return self.full_name()
    
  def date_of_birth_str(self):
    return self.date_of_birth.strftime("%d/%m/%Y")
    
  def sortBySurname(swimmer):
    return swimmer.last_name + ' ' + swimmer.first_name

  # Output the whole Swimmer in string format, with fields separated by '|' characters.
  # This is mirrored in swimmer.js
  def __str__(self):
    gender = "F"
    if self.is_male:
      gender = "M"
    return str( self.asa_number ) + "|" + self.last_name + "|" + self.first_name + "|" + self.known_as + "|" + gender + "|" + self.date_of_birth_str()
