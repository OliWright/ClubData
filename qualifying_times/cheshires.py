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

age_on_date_str = '31/12/2020'
earliest_pb_date_str = '2/1/2019'
is_long_course = False
prefer_qualifying_times_in_target_course = False

max_qualifying_meet_level = 4

BOYS_SPREADSHEET_DATA_STR = """50 Free	36.5	36.5	34	32	30	29	28.5	26.5
100 Free	1.20.00	1.20.00	1:16.50	1:10.5	1:08.00	1:06.38	1:02.52	59.04
200 Free	2:52.6	2:52.6	2:46.00	2:35.0	2:29.0	2:23.89	2:19.27	2:13.00
400 Free	6.00.00	6.00.00	5:40.0	5:24.5	5:11.0	5:00.0	5:00.0	4:45.0
800 Free	0	0	11:30.0	10:50.0	10:40.0	10:20.0	10:10.0	10:00.0
1500 Free	0	0	22.50.00	21:30.0	20:40.0	19:50.0	19.25.00	18:45.00
50 Back	42	42	39.5	37	35	34.5	34	31.5
100 Back	1.33.00	1.33.00	1:27.00	1:21.5	1:17.0	1:12.5	1:11.5	1:08.5
200 Back	3:11.30	3:11.30	3.04.68	2:56.00	2:46.4	2:41.50	2:41.00	2:35.5
50 Breast	49	49	45.5	43	41	40	38.5	36
100 Breast	1:46.0	1:46.0	1:38.0	1:32.0	1:31.00	1:26.6	1:24.20	1:20.0
200 Breast	3:46.0	3:46.0	3:40.00	3:28.00	3:18.18	3:08.8	3:05.0	2:58.0
50 Fly	43	43	39.5	37	35	33	32.5	29
100 Fly	1.41.00	1.41.00	1:35.0	1:26.0	1:20.00	1:15.50	1:12.00	1:09.00
200 Fly	3:46.1	3:46.1	3:27.7	3.10.00	2:53.00	2:44.86	2:38.00	2:34.20
100 IM	1:33.0	1:33.0	1.25.60	1:22.0	1.17.50	1.15.50	1.13.50	1.10.00
200 IM	3:24.00	3:24.00	3:11.8	2:56.3	2:49.6	2:42.5	2:40.60	2:32.0
400 IM	0	0	6:45.3	6:16.0	5:57.0	5:45.10	5:41.0	5:30.0"""

GIRLS_SPREADSHEET_DATA_STR = """50 Free	37	37	34	32	31	31	30.5	30.5
100 Free	1.22.00	1.22.00	1.17.00	1.11.50	1.08.50	1.08.50	1:08.00	1:08.00
200 Free	2.55.00	2.55.00	2.46.10	2.35.00	2.29.00	2.27.50	2:27.00	2:26.00
400 Free	6.03.00	6.03.00	5.45.10	5.25.00	5.15.00	5.09.00	5.09.00	5.09.00
800 Free	0	0	11.30.00	10.50.00	10.40.00	10.40.00	10:40.00	10:35.00
1500 Free	0	0	22.50.00	21.30.00	21.00.00	20.30.00	20.15.00	20.00.00
50 Back	42	42	40	37	35.5	35	35	35
100 Back	1.33.00	1.33.00	1.28.00	1.21.50	1:17.00	1:17.00	1:17.00	1:16.50
200 Back	3.16.30	3.16.30	3.06.90	2.56.00	2:46.50	2:43.70	2:43.20	2:41.30
50 Breast	49	49	45.5	43	41.5	40.5	40.5	40.5
100 Breast	1.47.00	1.47.00	1.42.00	1.35.00	1:31.00	1:29.00	1:29.00	1:29.00
200 Breast	3.48.70	3.48.70	3.40.80	3.28.50	3:19.00	3:15.80	3:13.80	3:12.40
50 Fly	43	43	39.5	37	35	34	34	34
100 Fly	1.41.00	1.41.00	1.35.00	1.26.00	1:20.90	1:18.90	1:18.90	1:17.00
200 Fly	3.50.00	3.50.00	3.28.00	3.10.50	2.57.20	2:53.30	2:53.00	2:53.00
100 IM	1.33.00	1.33.00	1.25.60	1.22.00	1.19.00	1.18.00	1.18.00	1.18.00
200 IM	3.24.00	3.24.00	3.12.20	2.56.50	2:51.00	2:47.00	2:47.00	2:47.00
400 IM	0	0	6.45.60	6.16.50	6.00.00	5.57.00	5.57.00	5.57.00"""

