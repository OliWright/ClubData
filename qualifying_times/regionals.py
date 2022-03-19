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

age_on_date_str = '31/12/2022'
earliest_pb_date_str = '1/1/2020'
is_long_course = True
prefer_qualifying_times_in_target_course = True

max_qualifying_meet_level = 4

BOYS_SPREADSHEET_DATA_STR = """50 Free	34.4	31.9	29.49	28.4	27.5	25.1
100 Free	1:16.90	1:11.00	1:04.50	1:02.10	1:00.20	54.7
200 Free	2:55.00	2:35.30	2:21.40	2:15.90	2:13.80	1:59.30
400 Free	6:53.50	5:44.30	5:11.00	4:52.60	4:45.10	4:16.60
800 Free	12:19.70	11:15.80	10:26.30	10:05.20	9:40.70	9:09.10
1500 Free	22:06.80	21:48.50	19:51.20	19:33.00	18:45.90	17:35.10
50 Back	40.1	37.1	34.6	33.3	32	28.5
100 Back	1:27.10	1:21.20	1:15.10	1:12.60	1:09.00	1:01.30
200 Back	3:28.90	3:01.50	2:42.70	2:39.50	2:30.30	2:15.10
50 Breast	47.1	42.7	39.1	37.4	34.9	32.2
100 Breast	1:44.00	1:35.80	1:25.70	1:22.30	1:17.80	1:09.90
200 Breast	3:59.80	3:33.10	3:08.90	3:05.30	2:51.10	2:36.70
50 Fly	39.7	36.1	32.3	31.1	30.2	27.1
100 Fly	1:42.50	1:28.20	1:13.80	1:10.90	1:08.40	59.6
200 Fly	3:38.00	3:14.60	2:48.00	2:33.00	2:28.80	2:16.40
200 IM	3:19.00	2:58.10	2:40.20	2:36.70	2:29.60	2:15.90
400 IM	7:43.00	6:13.40	5:43.40	5:25.20	5:11.40	4:51.00"""

GIRLS_SPREADSHEET_DATA_STR = """50 Free	33.7	31.6	30.7	29.9	29.8	28.4
100 Free	1:14.50	1:09.30	1:06.80	1:05.60	1:04.70	1:01.30
200 Free	2:43.40	2:29.20	2:23.60	2:22.40	2:19.00	2:14.30
400 Free	6:14.20	5:22.10	5:11.90	5:05.50	4:53.80	4:43.20
800 Free	12:23.20	11:39.70	11:18.00	10:40.00	10:08.10	9:51.90
1500 Free	23:14.90	22:55.70	22:19.40	22:09.40	21:31.50	20:13.50
50 Back	38.7	36.5	35.1	34.1	33.5	32.3
100 Back	1:25.50	1:19.20	1:15.00	1:13.90	1:12.00	1:09.30
200 Back	3:13.20	2:51.00	2:41.50	2:39.60	2:35.00	2:29.60
50 Breast	44.9	41.9	39.5	38.9	38.5	36
100 Breast	1:39.60	1:31.00	1:27.00	1:25.60	1:24.80	1:18.80
200 Breast	3:35.80	3:13.50	3:09.80	3:07.20	3:02.60	2:49.10
50 Fly	38	35.1	33.4	32.8	31.9	30.7
100 Fly	1:33.00	1:21.90	1:15.70	1:14.90	1:11.70	1:08.10
200 Fly	4:00.40	3:47.30	3:29.30	3:05.50	2:47.40	2:36.60
200 IM	3:05.10	2:49.50	2:42.80	2:42.80	2:36.80	2:29.70
400 IM	6:51.20	6:33.50	6:03.00	5:49.40	5:36.70	5:21.90"""

BOYS_CONSIDERATION_TIMES_STR = None
GIRLS_CONSIDERATION_TIMES_STR = None
