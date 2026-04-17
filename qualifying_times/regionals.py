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
min_age = 12 # 11/12
max_age = 17

age_on_date_str = '31/12/2026'
earliest_pb_date_str = '5/5/2025'
latest_pb_date_youth_str = '17/3/2026'
latest_pb_date_senior_str = '17/3/2026'
is_long_course = True
prefer_qualifying_times_in_target_course = False
round_down_conversions = True

max_qualifying_meet_level = 3

BOYS_SPREADSHEET_DATA_STR = """50 Free	00:33.59	00:30.99	00:29.59	00:28.59	00:27.59	00:25.99
100 Free	01:12.59	01:07.59	01:03.59	01:00.99	00:58.99	00:56.59
200 Free	02:37.99	02:26.99	02:18.99	02:14.99	02:10.99	02:05.59
400 Free	05:39.99	05:17.99	04:57.99	04:48.59	04:44.59	04:34.99
800 Free	11:29.99	10:39.99	10:05.99	09:49.99	09:40.99	09:24.99
1500 Free	21:29.99	20:34.99	19:24.99	18:48.59	18:30.99	18:09.99
50 Breast	00:43.99	00:39.99	00:37.99	00:35.99	00:34.59	00:33.59
100 Breast	01:37.99	01:30.99	01:23.59	01:19.99	01:17.59	01:13.99
200 Breast	03:29.99	03:14.99	03:01.99	02:52.99	02:50.59	02:44.99
50 Fly	00:36.99	00:33.99	00:31.99	00:30.59	00:28.99	00:27.99
100 Fly	01:32.99	01:20.59	01:12.99	01:08.99	01:06.59	01:03.59
200 Fly	03:18.99	03:05.59	02:50.99	02:35.99	02:32.99	02:27.59
50 Back	00:38.99	00:35.99	00:33.59	00:31.99	00:31.59	00:29.59
100 Back	01:22.59	01:18.59	01:12.99	01:09.59	01:08.59	01:06.59
200 Back	03:02.99	02:48.99	02:37.99	02:30.99	02:29.99	02:23.99
200 IM	03:00.99	02:48.59	02:39.59	02:32.59	02:29.99	02:28.59
400 IM	06:24.99	06:05.99	05:45.99	05:35.99	05:25.99	05:15.99"""

GIRLS_SPREADSHEET_DATA_STR = """50 Free	00:32.59	00:31.59	00:29.99	00:29.59	00:28.99	00:28.59
100 Free	01:11.59	01:07.59	01:05.59	01:04.59	01:03.59	01:01.99
200 Free	02:36.59	02:26.99	02:22.99	02:19.99	02:17.99	02:14.99
400 Free	05:33.99	05:15.99	04:59.99	04:57.99	04:55.59	04:49.99
800 Free	11:24.99	10:42.99	10:15.99	10:04.99	09:57.99	09:49.99
1500 Free	21:29.99	20:34.99	19:59.99	19:09.99	18:59.99	18:44.99
50 Breast	00:42.59	00:40.59	00:38.99	00:38.59	00:37.99	00:36.99
100 Breast	01:33.99	01:28.99	01:26.59	01:24.59	01:23.59	01:21.59
200 Breast	03:22.59	03:13.59	03:06.99	03:03.99	03:02.99	02:58.99
50 Fly	00:35.99	00:34.59	00:32.99	00:31.99	00:31.59	00:30.99
100 Fly	01:25.99	01:18.99	01:14.99	01:12.59	01:11.59	01:08.99
200 Fly	03:18.99	03:05.59	02:51.99	02:41.99	02:40.99	02:39.99
50 Back	00:38.59	00:35.99	00:34.99	00:34.59	00:33.59	00:32.59
100 Back	01:21.99	01:16.99	01:14.59	01:12.59	01:10.99	01:09.59
200 Back	02:56.59	02:45.99	02:39.99	02:36.99	02:35.59	02:32.99
200 IM	02:56.99	02:48.59	02:42.59	02:39.99	02:37.99	02:33.99
400 IM	06:24.99	06:05.99	05:49.99	05:40.99	05:39.99	05:35.99"""

BOYS_CONSIDERATION_TIMES_STR = None
GIRLS_CONSIDERATION_TIMES_STR = None
