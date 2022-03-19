input_folder = 'input/'
output_folder = 'output/'

class Lane():
	def __init__(self, tokens):
		self.number = int(tokens[0])
		self.name = tokens[1]
		if len(self.name) == 0:
			# Empty lane
			self.name = None
			self.distance = None
			self.stroke = None
		else:
			self.event_name = tokens[2]
			event_tokens = self.event_name.split(' ')
			self.distance = int(event_tokens[0])
			self.stroke = event_tokens[1]

class Event():
	def __init__(self, number):
		self.number = number
		self.lanes = []
		self.distance = None
		self.stroke = None

	def add_lane(self, lane):
		self.lanes.append(lane)
		if self.distance is None:
			self.distance = lane.distance
			self.stroke = lane.stroke
		elif lane.name is not None:
			assert(self.distance == lane.distance)
			if self.stroke != lane.stroke:
				self.stroke = "Mixed"
		return lane.number

current_lane = 0
reading_event = False
events = []
event = None

scb_name_width = 20
scb_club_width = 16

# Read the file
heats_file = open( input_folder + 'Level X - Session 1.tsv', 'r' )
for line in heats_file:
	tokens = line.split('\t')
	print(tokens)
	if reading_event:
		if event.add_lane(Lane(tokens)) == 6:
			reading_event = False
	else:
		if line.startswith("Heat"):
			event_number = int(tokens[0].split(' ')[1])
			event = Event(event_number)
			events.append(event)
			reading_event = True
			current_lane = 1

schedule_file = open( output_folder + 'generic.sch', 'w')
for event in events:
	if event.distance is not None:
		# Write the generic.sch file

		# Event Number
		schedule_file.write(str(event.number)+';')
		# Event Description
		event_description = 'Mixed {0} {1}'.format(event.distance, event.stroke)
		schedule_file.write(event_description + ';')
		# Number of splits (pad touches)
		schedule_file.write(str(event.distance//25) + ';')
		# Gender (F/M/X)
		schedule_file.write('M' + ';')
		# Low Age
		schedule_file.write('7' + ';')
		# High Age
		schedule_file.write('21' + ';')
		# Distance
		schedule_file.write(str(event.distance) + ';')
		# Stroke Code (A=Free, B=Back, C=Breast, 4=Fly, 5=Medley)
		code = '5'
		if event.stroke == 'Free':
			code = 'A'
		elif event.stroke == 'Back':
			code = 'B'
		elif event.stroke == 'Breast':
			code = 'C'
		elif event.stroke == 'Fly':
			code = '4'
		schedule_file.write(code + ';')
		# Individual/Relay Code (I=Individual, R=Relay)
		schedule_file.write('I' + ';')
		# Round Code (P=Prelims, S=Semifinals, F=Finals)		
		schedule_file.write('F' + ';')
		schedule_file.write('\n')

		# Write the scoreboard file
		scb_file_name = 'E{0:03}.scb'.format(event.number)
		scb_file = open( output_folder + scb_file_name, 'w')
		scb_file.write('#{0:03} {1}\n'.format(event.number, event_description))
		for lane_num in range(10):
			name = ''
			club = ''
			if lane_num < len(event.lanes):
				lane = event.lanes[lane_num]
				if lane.name is not None:
					name = lane.name
				club = 'WINN'
			if len(name) > scb_name_width:
				# Truncate the name
				name = name[0:scb_name_width]
			scb_file.write('{0: <20}--{1: <16}\n'.format(name, club))
		scb_file.close()
schedule_file.close()