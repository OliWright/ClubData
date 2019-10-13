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

age_on_date_str = '31/12/2019'
earliest_pb_date_str = '1/6/2018'
is_long_course = True

max_qualifying_meet_level = 2
excluded_meets = {
"Winsford  Club Championships",
"Winsford  Time Trial",
"Winsford Swim Team Club Champs",
"Winsford Club Championships 2017",
"Winsford Swim Team Club Championships 2018",
"Winsford Reverse 800/1500m Event"
}

BOYS_SPREADSHEET_DATA_STR = """50 Free	32.09	30.09	29.09	27.99	27.89	26.09
100 Free	1:09.59	1:04.29	1:01.89	59.39	58.69	56.79
200 Free	2:28.49	2:20.49	2:14.29	2:08.19	2:06.69	2:04.49
400 Free	5:13.39	4:56.79	4:44.99	4:34.69	4:29.99	4:29.29
800 Free	10:35.09	10:00.09	9:40.09	9:20.09	9:10.09	9:00.09
1500 Free	20:44.39	19:39.69	18:58.89	18:22.59	18:03.79	18:01.99
50 Back	37.09	35.59	34.39	32.89	32.09	31.29
100 Back	1:17.19	1:13.79	1:09.09	1:06.59	1:05.29	1:05.09
200 Back	2:47.89	2:42.59	2:30.09	2:24.19	2:20.89	2:20.69
50 Breast	40.99	39.69	38.39	36.59	35.89	33.39
100 Breast	1:30.39	1:25.69	1:20.59	1:15.89	1:15.19	1:11.79
200 Breast	3:11.49	3:02.59	2:52.19	2:44.69	2:42.69	2:36.19
50 Fly	35.89	33.69	31.69	30.69	29.99	28.09
100 Fly	1:15.19	1:11.79	1:08.39	1:03.89	1:03.79	1:02.19
200 Fly	3:03.59	2:52.59	2:38.99	2:26.59	2:23.99	2:19.29
200 IM	2:47.29	2:39.99	2:32.89	2:26.89	2:23.49	2:22.79
400 IM	5:54.19	5:41.49	5:31.59	5:14.89	5:08.19	5:07.99"""

GIRLS_SPREADSHEET_DATA_STR = """50 Free	32.09	31.39	30.89	30.49	30.29	30.09
100 Free	1:09.19	1:07.19	1:05.89	1:04.59	1:04.49	1:02.69
200 Free	2:29.69	2:24.59	2:21.99	2:19.29	2:17.69	2:17.19
400 Free	5:15.39	5:04.19	5:00.09	4:54.09	4:53.89	4:53.59
800 Free	10:50.29	10:27.89	10:14.69	10:06.09	10:05.89	10:05.59
1500 Free	21:13.19	20:30.59	19:50.59	19:15.59	19:00.29	18:55.59
50 Back	37.29	36.19	35.39	34.39	34.29	34.19
100 Back	1:18.89	1:15.49	1:13.39	1:11.69	1:11.49	1:11.39
200 Back	2:47.89	2:40.59	2:37.49	2:33.89	2:33.29	2:32.79
50 Breast	41.59	40.09	38.99	38.09	37.89	37.69
100 Breast	1:28.29	1:24.89	1:23.69	1:22.59	1:22.49	1:22.29
200 Breast	3:10.99	3:01.59	3:00.89	3:00.39	2:58.09	2:57.39
50 Fly	34.59	34.09	33.19	32.19	32.09	31.59
100 Fly	1:17.99	1:13.79	1:12.09	1:10.69	1:10.59	1:09.99
200 Fly	2:59.59	2:53.59	2:42.59	2:37.59	2:35.79	2:35.59
200 IM	2:50.09	2:42.59	2:41.79	2:38.39	2:37.79	2:35.19
400 IM	6:02.39	5:49.19	5:39.39	5:36.69	5:36.49	5:35.49"""

