# Noddy code to read a csv into an array of objects, assuming the first line is a header
#   read_csv_with_header.py
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

def read_csv_with_header(file_name):
  file = open(file_name, 'r')
  if file is None:
    print('Failed to open file: ' + file_name)
    return
  
  headers = None
  rows = []
  for line in file:
    tokens = line.split(',')
    if headers is None:
      headers = tokens
      num_columns = len(headers)
    else:
      row = {}
      num_entries = len(tokens)
      if num_entries > num_columns:
        num_entries = num_columns
      for i in range(num_entries):
        row[headers[i]] = tokens[i]
        #print(headers[i])
      rows.append(row)
  return rows