import sys
from variables import *
from file_process import *

# argument 1: variables path
# argument 2: result path
# argument 3: solved path
argument_count = 3

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
    value = int(line.split()[1])
    newLine = line.split()[0] + " " + str(value in numbers)
    appendLineOutput(newLine, solvedPath, addZero=False)
