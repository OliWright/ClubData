file = open('C:\\Users\\Sue\\Downloads\\2022-09-24_0927-Winsford_ASC_Club_Championships_2022-heat-sheets (1).csv', 'r')

include_club = False

heat = 0

for line in file:
  # Strip the
  line = line.strip('\n')

  tokens = line.split(',')
  if len(tokens) > 2:
    # Heat header or lane
    if tokens[0] != 'Heat':
      this_heat = int(tokens[0])
      if this_heat != heat:
        # Change of heat
        heat = this_heat
        print('Heat ' + str(heat))
        if include_club:
          print('Lane\tSwimmer\tClub\tAge\Entry Time')
        else:
          print('Lane\tSwimmer\tAge\t\tEntry Time')
      if include_club:
        print(tokens[1] +'\t' + tokens[2] +'\t' + tokens[3] +'\t' + tokens[4] +'\t' + tokens[5])
      else:
        print(tokens[1] +'\t' + tokens[2] +'\t' + tokens[4] +'\t\t' + tokens[5])
  elif line[0:3].isdigit():
    # Event header
    print(line)
    heat = 0
