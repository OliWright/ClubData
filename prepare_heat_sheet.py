file = open('C:\\Users\\Sue\\Downloads\\2022-02-19_1339-Winsford_Time_Trial_19th_February_2022-heat-sheets.csv', 'r')

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
        print('Lane\tSwimmer\tAge\tEntry Time')
      print(tokens[1] +'\t' + tokens[2] +'\t' + tokens[4] +'\t' + tokens[5])
  elif line[0:3].isdigit():
    # Event header
    print(line)
    heat = 0
