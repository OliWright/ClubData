import sys
sys.path.append("modules")

import read_club_rankings
import swim_data_sheets

swimmers = read_club_rankings.ReadClubRankingsFiles()
swim_data_sheets.UpdateSwimmerData(swimmers)