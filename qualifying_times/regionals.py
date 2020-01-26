# Winsford ASC Club Champs Scoring System
#   regionals.py
#   Qualifying times for the regionals
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

# Table
min_age = 12
max_age = 17

age_on_date_str = '31/12/2020'
earliest_pb_date_str = '1/4/2019'
is_long_course = True
prefer_qualifying_times_in_target_course = True

max_qualifying_meet_level = 3

BOYS_SPREADSHEET_DATA_STR = """50 Free	32.98	30.82	29.78	27.99	27.89	26.09
100 Free	1.12.09	1.06.99	1.03.29	59.39	58.69	56.79
200 Free	2.34.69	2.25.49	2.17.79	2.08.19	2.06.69	2.04.49
400 Free	5.33.29	5.10.19	4.52.63	4.34.69	4.29.99	4.29.29
800 Free	10.50.09	10.15.09	9.55.09	9.35.09	9.25.09	9.15.09
1500 Free	21.04.39	19.59.69	19.18.89	18.22.59	18.03.79	18.01.99
50 Back	37.59	35.59	33.71	32.59	32.09	31.19
100 Back	1.22.09	1.16.39	1.11.29	1.06.59	1.05.29	1.05.09
200 Back	2.57.09	2.43.39	2.35.09	2.24.19	2.20.89	2.20.69
50 Breast	42.99	40.29	37.66	36.59	35.89	33.39
100 Breast	1.33.49	1.27.99	1.22.79	1.15.89	1.15.19	1.11.79
200 Breast	3.20.29	3.10.59	2.59.89	2.44.69	2.42.69	2.36.19
50 Fly	36.92	34.81	31.81	30.69	29.99	28.09
100 Fly	1.21.09	1.17.99	1.10.29	1.03.89	1.03.79	1.02.19
200 Fly	3.08.99	2.57.30	2.45.99	2.26.59	2.23.99	2.19.29
200 IM	2.56.89	2.47.39	2.37.69	2.26.89	2.23.49	2.22.79
400 IM	5.54.19	5.41.49	5.31.59	5.14.89	5.08.19	5.07.99"""

GIRLS_SPREADSHEET_DATA_STR = """50 Free	33.06	31.39	30.89	30.49	30.29	30.09
100 Free	1.12.89	1.08.19	1.05.89	1.04.59	1.04.49	1.02.69
200 Free	2.35.69	2.26.89	2.21.99	2.19.29	2.17.69	2.17.19
400 Free	5.30.89	5.15.99	5.00.09	4.54.09	4.53.89	4.53.59
800 Free	11.05.29	10.42.89	10.29.69	10.06.09	10.00.09	9.58.09
1500 Free	21.13.19	20.30.59	19.50.59	19.15.59	18.59.09	18.40.09
50 Back	38.31	36.19	35.39	34.39	34.29	34.19
100 Back	1.22.69	1.17.19	1.13.19	1.11.69	1.11.39	1.11.09
200 Back	2.57.69	2.46.79	2.38.49	2.33.89	2.33.29	2.32.79
50 Breast	43.09	40.69	38.53	38.09	37.89	37.49
100 Breast	1.33.59	1.28.69	1.24.39	1.21.99	1.21.59	1.21.09
200 Breast	3.20.39	3.11.09	3.00.89	2.59.49	2.58.09	2.57.39
50 Fly	36.19	34.16	33.19	32.19	32.09	31.59
100 Fly	1.23.09	1.18.39	1.12.09	1.10.69	1.10.59	1.09.99
200 Fly	3.08.99	2.58.09	2.42.59	2.37.59	2.35.79	2.35.59
200 IM	2.57.09	2.47.99	2.41.79	2.38.39	2.37.79	2.35.19
400 IM	6.02.39	5.49.19	5.39.39	5.36.69	5.36.49	5.35.49"""

