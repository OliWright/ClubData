# Winsford ASC Club Champs Scoring System
#   winter regionals.py
#   Qualifying times for the winter regionals
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
min_age = 14
max_age = 17

age_on_date_str = '31/12/2025'
earliest_pb_date_str = '1/4/2024'
is_long_course = False
prefer_qualifying_times_in_target_course = False
round_down_conversions = True

max_qualifying_meet_level = 3

BOYS_SPREADSHEET_DATA_STR = """50 Free	00:25.91	00:25.91	00:25.91	00:25.86
100 Free	00:58.66	00:56.77	00:56.77	00:56.51
200 Free	02:08.11	02:05.31	02:05.31	02:04.99
400 Free	04:33.15	04:29.57	04:29.57	04:27.21
800 Free	09:30.94	09:30.94	09:30.94	09:15.61
1500 Free	19:00.35	19:00.35	19:00.35	19:00.35
50 Back	00:29.82	00:29.82	00:29.82	00:29.82
100 Back	01:07.12	01:04.81	01:04.81	01:04.54
200 Back	02:26.28	02:22.81	02:22.81	02:21.36
50 Breast	00:32.68	00:32.68	00:32.68	00:32.61
100 Breast	01:17.66	01:12.41	01:12.41	01:11.66
200 Breast	02:46.88	02:43.99	02:43.99	02:39.56
50 Fly	00:28.12	00:28.12	00:28.12	00:27.88
100 Fly	01:07.08	01:03.98	01:03.98	01:03.04
200 Fly	02:43.34	02:29.33	02:29.33	02:24.81
100 IM	01:09.39	01:07.21	01:07.21	01:05.85
200 IM	02:27.68	02:22.33	02:22.33	02:20.38
400 IM	05:15.01	05:14.01	05:14.01	05:11.73"""

GIRLS_SPREADSHEET_DATA_STR = """50 Free	00:28.65	00:28.65	00:28.65	00:28.73
100 Free	01:02.33	01:01.59	01:01.59	01:01.19
200 Free	02:14.72	02:14.18	02:14.18	02:12.75
400 Free	04:43.98	04:42.78	04:42.78	04:39.08
800 Free	09:51.17	09:51.17	09:51.17	09:48.17
1500 Free	19:11.35	19:11.35	19:11.35	19:11.35
50 Back	00:32.57	00:32.57	00:32.57	00:31.94
100 Back	01:10.42	01:09.76	01:09.76	01:08.41
200 Back	02:31.88	02:31.42	02:31.42	02:30.27
50 Breast	00:37.21	00:37.21	00:37.21	00:37.05
100 Breast	01:21.19	01:21.04	01:21.04	01:19.45
200 Breast	02:54.05	02:56.88	02:56.88	02:55.61
50 Fly	00:31.24	00:31.24	00:31.24	00:30.99
100 Fly	01:10.12	01:09.78	01:09.78	01:08.63
200 Fly	02:34.99	02:32.63	02:32.63	02:39.94
100 IM	01:11.82	01:11.75	01:11.75	01:11.23
200 IM	02:33.39	02:33.12	02:33.12	02:31.77
400 IM	05:24.86	05:18.67	05:18.67	05:22.69"""

BOYS_CONSIDERATION_TIMES_STR = None
GIRLS_CONSIDERATION_TIMES_STR = None
