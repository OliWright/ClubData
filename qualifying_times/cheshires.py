# Winsford ASC Club Champs Scoring System
#   cheshires.py
#   Qualifying times for the cheshires
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

min_age = 10
max_age = 17

age_on_date_str = '31/12/2022'
earliest_pb_date_str = '2/1/2020'
is_long_course = False
prefer_qualifying_times_in_target_course = False

max_qualifying_meet_level = 4

BOYS_SPREADSHEET_DATA_STR = """50 Free	35	35	34	32	30	28.5	28	26.5
100 Free	1.18.00	1.18.00	1.13.00	1.08.00	1:05.00	1:02.50	1:00.00	57
200 Free	2.50.00	2.50.00	2.40.00	2.30.00	2:20.00	2:15.00	2:14.00	2:11.00
400 Free	5.40.00	5.40.00	5.30.00	5.20.00	5:05.00	4.50.00	4.45.00	4:40.00
800 Free	0	0	0	0	0	0	0	0
1500 Free	0	0	22.00.00	22.30.00	20.00.00	19.30.00	18.50.00	18:30.00
50 Back	41	41	39	36	34.5	33	32.5	31.5
100 Back	1.31.00	1.31.00	1:25.00	1.21.00	1.16.50	1.12.50	1.11.50	1.08.50
200 Back	3.00.00	3.00.00	2.55.00	2.50.00	2.45.00	2.40.00	2.37.00	2:34.00
50 Breast	49	49	45	42.5	40	37.8	37	35.5
100 Breast	1.44.00	1.44.00	1:38.00	1.32.00	1.28.00	1.26.60	1:24.20	1:20.00
200 Breast	3.46.00	3:46.00	3:40.00	3.28.00	3.18.00	3.08.80	3.05.00	3.00.00
50 Fly	43	43	39.5	37	35	33	32.5	29
100 Fly	1.35.00	1.35.00	1:29.00	1:23.00	1.17.50	1.14.00	1:11.00	1:08.00
200 Fly	3.35.00	3.35.00	3.15.00	3.00.00	2.53.00	2:44.86	2:38.00	2:34.20
100 IM	1.33.00	1.33.00	1.25.60	1.22.00	1.17.50	1.15.50	1.13.50	1.10.00
200 IM	3.15.00	3.15.00	3.05.00	2.55.00	2:45.00	2:40.00	2:35.00	2:30.00
400 IM	0	0	6.25.00	6.00.00	5.40.00	5:35.00	5.35.00	5:20.00"""

GIRLS_SPREADSHEET_DATA_STR = """50 Free	35	35	32.5	31	30.5	30.5	30.5	30
100 Free	1.17.00	1.17.00	1.13.00	1.09.50	1.07.50	1.06.00	1:06.00	1:06.00
200 Free	2.50.00	2.50.00	2.40.00	2.30.00	2.26.00	2.24.00	2:24.00	2:24.00
400 Free	5.40.00	5.40.00	5.25.00	5.20.00	5.10.00	5.02.50	5.02.50	5.02.50
800 Free	0	0	11.00.00	10.35.00	10.25.00	10.20.00	10:20.00	10:20.00
1500 Free	0	0	0	0	0	0	0	0
50 Back	40	40	38	36	35	34.5	34.5	34.5
100 Back	1.29.00	1.29.00	1.24.00	1.20.00	1:17.00	1:17.00	1:16.00	1:16.00
200 Back	3.08.00	3.08.00	2.58.00	2.51.00	2:45.00	2:42.00	2:42.00	2:42.00
50 Breast	48	48	45	42.5	41	40.5	40.5	40.5
100 Breast	1.45.00	1.45.00	1.40.00	1.33.00	1:30.00	1:29.00	1:29.00	1:29.00
200 Breast	3.45.00	3.45.00	3.40.00	3.28.50	3:20.00	3:17.00	3:17.00	3:17.00
50 Fly	40	40	38.5	36	35	34	33.5	33
100 Fly	1.35.00	1.35.00	1.28.00	1.20.00	1:17.50	1:17.50	1:16.50	1:16.00
200 Fly	3.35.00	3.35.00	3.10.00	3.00.00	2.57.00	2:53.30	2:53.00	2:53.00
100 IM	1.31.00	1.31.00	1.25.60	1.21.00	1.16.50	1.16.50	1.16.50	1.16.50
200 IM	3.20.00	3.20.00	3.05.00	2.56.50	2:51.00	2:45.00	2:45.00	2:45.00
400 IM	0	0	6.25.00	6.05.00	5.55.00	5.50.00	5.50.00	5.50.00"""

