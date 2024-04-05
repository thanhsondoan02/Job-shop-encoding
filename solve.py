import sys
from variables import *
from file_process import *
from variables import StartAfter, isStartAfter

# argument 1: variables path
# argument 2: result path
# argument 3: solved path
argument_count = 3
startTimeDict = {}

if len(sys.argv) != argument_count + 1:
  print("Please provide", argument_count, "arguments")
else:
  variablePath = sys.argv[1]
  resultPath = sys.argv[2]
  solvedPath = sys.argv[3]

  with open(resultPath, 'r') as file:
    content = file.read().split()
  numbers = [int(x) for x in content if x.lstrip('-').isdigit()]
  numbers = numbers[:-1]  # always remove last number 0

  with open(variablePath, 'r') as file:
    lines = file.readlines()

  clearFileContent(solvedPath)
  for line in lines:
    try:
      var = StartAfter(line.split()[0])
    except:
      continue
    value = int(line.split()[1]) in numbers  # true or false
    if value == True:
      if (var.jobIndex, var.opeIndex) not in startTimeDict:
        startTimeDict[(var.jobIndex, var.opeIndex)] = var.time
      else:
        if var.time > startTimeDict[(var.jobIndex, var.opeIndex)]:
          startTimeDict[(var.jobIndex, var.opeIndex)] = var.time
  # for item in startTimeDict.items():

  #   newL
  #   appendLineOutput(newLine, solvedPath, addZero=False)
  # print(startTimeDict)
  for i in startTimeDict.keys():
    newLine = f"({i[0]},{i[1]}): {startTimeDict[i]}"
    appendLineOutput(newLine, solvedPath, addZero=False)
