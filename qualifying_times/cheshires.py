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

age_on_date_str = '31/12/2026'
earliest_pb_date_str = '2/2/2025'
is_long_course = False
prefer_qualifying_times_in_target_course = False
round_down_conversions = True

max_qualifying_meet_level = 4

# Qualifying times

BOYS_SPREADSHEET_DATA_STR = """50 Free	36.5	36.5	34	32	30	28.5	28	26.5
100 Free	1.21.00	1.21.00	1.16.00	1.10.00	1:06.00	1:03.50	1:01.50	57
200 Free	2.52.60	2.52.60	2.44.00	2.31.00	2:25.00	2:20.00	2:14.00	2:10.00
400 Free	6.03.00	6.03.00	5.45.00	5.22.00	5:00.00	4.55.00	4.50.00	4:35.00
800 Free			11.30.00	11.00.00	10.35.00	10.20.00	10.10.00	10.00.00
1500 Free			22.50.00	21.50.00	20.20.00	19.40.00	19.00.00	18:00.00
50 Back	43	43	41	38	35.5	33.5	33.5	32.5
100 Back	1.33.00	1.33.00	1:26.00	1.21.50	1.17.00	1.12.50	1.11.50	1.08.50
200 Back	3.15.30	3.15.30	3.02.00	2.54.00	2.45.00	2.40.00	2.38.00	2:31.00
50 Breast	49	49	45.5	42	40	38	37	35
100 Breast	1.46.00	1.46.00	1:38.00	1.32.00	1.27.50	1.25.00	1:22.50	1:17.00
200 Breast	3.46.00	3:46.00	3:35.00	3.28.00	3.16.00	3.08.00	3.01.00	2.55.00
50 Fly	43	43	39.5	36	33	32	31.5	30
100 Fly	1.45.00	1.45.00	1:35.00	1:26.00	1.20.00	1.15.50	1:12.00	1:09.00
200 Fly	3.48.00	3.48.00	3.27.00	3.08.00	2.54.00	2:45.00	2:38.00	2:34.20
100 IM	1.33.00	1.33.00	1.25.60	1.20.00	1.16.50	1.13.50	1.11.00	1.09.00
200 IM	3.24.00	3.24.00	3.11.00	2.53.00	2:48.00	2:42.00	2:38.00	2:30.00
400 IM			6.30.00	6.05.00	5.50.00	5:44.00	5.35.00	5:25.00"""

GIRLS_SPREADSHEET_DATA_STR = """50 Free	36.5	36.5	34	32	30.5	31	30.5	30
100 Free	1.21.00	1.21.00	1.16.00	1.10.00	1.07.00	1.06.50	1:06.50	1:05.50
200 Free	2.55.00	2.55.00	2.44.00	2.31.00	2.27.00	2.24.00	2:24.00	2:24.00
400 Free	6.03.00	6.03.00	5.45.00	5.22.00	5.10.00	5.00.00	5.03.00	5.03.00
800 Free			11.30.00	11.00.00	10.35.00	10.35.00	10:30.00	10:35.00
1500 Free			22.50.00	21.50.00	20.30.00	20.30.00	20.15.00	20.00.00
50 Back	43	43	41	38	35.5	35	35	34
100 Back	1.33.00	1.33.00	1.26.00	1.21.50	1:18.00	1:16.00	1:15.50	1:15.00
200 Back	3.15.30	3.15.30	3.02.00	2.54.00	2:43.50	2:40.00	2:42.00	2:42.00
50 Breast	49	49	45	42	41.5	40	39.5	39
100 Breast	1.47.00	1.47.00	1.39.00	1.33.00	1:30.00	1:29.00	1:27.00	1:26.00
200 Breast	3.46.00	3.46.00	3.35.00	3.25.00	3.15.50	3:10.00	3:10.00	3:07.50
50 Fly	43	43	39.5	36	33.5	33	33	0
100 Fly	1.45.00	1.45.00	1.35.00	1.26.00	1:20.00	1:17.00	1:17.00	1:15.00
200 Fly	3.50.00	3.50.00	3.28.00	3.10.50	2.57.00	2:53.30	2:53.00	2:51.00
100 IM	1.33.00	1.33.00	1.26.00	1.20.00	1.17.50	1.16.50	1.16.00	1.15.50
200 IM	3.24.00	3.24.00	3.11.00	2.53.00	2:49.00	2:46.00	2:46.00	2:46.00
400 IM			6.30.00	6.05.00	5.50.00	5.48.00	5.48.00	5.48.00"""

# Consideration Times

BOYS_CONSIDERATION_TIMES_STR = None

GIRLS_CONSIDERATION_TIMES_STR = None
