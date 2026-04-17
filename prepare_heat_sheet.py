file = open('C:\\Users\\Sue\\Downloads\\2026-04-11_0902-Winsford_Spring_Development_Meet_2026-heat-sheets (1).csv', 'r')

include_club = True

# Search and replaces
replacements = [
  ("Individual Medley", "IM"),
  ("9 Yrs/Over ", ""),
  (",0.0", ",-"),
  (",0", ","),
  ("Stockport Mo", "Stockport"),
  ("N'wich Seals", "Nantwich"),
  ("Romiley Mari", "Romiley"),
  ("Newcastle St", "N'castle St"),
  ("Bolton Metro", "Bolton"),
  ("Chadderton", "Chadd'ton"),
]

heat = 0

for line in file:
  # Strip the
  line = line.strip('\n')

  for replacement in replacements:
    line = line.replace(replacement[0], replacement[1])

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
          print('Lane\tSwimmer\tClub\tAge\tTime')
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
