import sys
from variables import *
from file_process import *


class SolvedOperation:
  def __init__(self, jobIndex, opeIndex, machine, processingTime, startTime, endTime):
    self.jobIndex = jobIndex
    self.opeIndex = opeIndex
    self.machine = machine
    self.processingTime = processingTime
    self.startTime = startTime
    self.endTime = endTime


# argument 1: variables path
# argument 2: result path
# argument 3: solved path
# argument 4: problem path
argument_count = 4
startTimeDict = {}

if len(sys.argv) != argument_count + 1:
  print("Please provide", argument_count, "arguments")
else:
  variablePath = sys.argv[1]
  resultPath = sys.argv[2]
  solvedPath = sys.argv[3]
  problemPath = sys.argv[4]

  with open(resultPath, 'r') as file:
    content = file.read().split()
  numbers = [int(x) for x in content if x.lstrip('-').isdigit()]
  numbers = numbers[:-1]  # always remove last number 0

  with open(variablePath, 'r') as file:
    lines = file.readlines()

  clearFileContent(solvedPath)
  for line in lines:
    try:
      var = stringToStartAfter(line.split()[0])
    except:
      continue
    value = int(line.split()[1]) in numbers  # true or false
    if value == True:
      if (var.jobIndex, var.opeIndex) not in startTimeDict:
        startTimeDict[(var.jobIndex, var.opeIndex)] = var.time
      else:
        if var.time > startTimeDict[(var.jobIndex, var.opeIndex)]:
          startTimeDict[(var.jobIndex, var.opeIndex)] = var.time
  _, _, jobs = jobsFromFile(problemPath)

  # map to other properties: machine, processingTime, startTime, endTime
  solvedOperations = []
  for i in startTimeDict.keys():
    jobIndex = i[0]
    opeIndex = i[1]
    machine = jobs[jobIndex][opeIndex][0]
    processingTime = jobs[jobIndex][opeIndex][1]
    startTime = startTimeDict[i]
    endTime = startTime + processingTime
    solvedOperations.append(SolvedOperation(
        jobIndex, opeIndex, machine, processingTime, startTime, endTime))

  # sort by job index and operation index
  sortedSolvedOperations = sorted(solvedOperations, key=lambda x: (x.jobIndex, x.opeIndex))
  for i in sortedSolvedOperations:
    jobIndex = i.jobIndex
    opeIndex = i.opeIndex
    machine = i.machine
    processingTime = i.processingTime
    startTime = i.startTime
    endTime = i.endTime
    newLine = f"({jobIndex},{opeIndex}): {machine} {processingTime} {startTime} {endTime}"
    appendLineOutput(newLine, solvedPath, addZero=False)

  appendLineOutput("\n\n", solvedPath, addZero=False)

  # sort by machine and start time
  sortedSolvedOperations = sorted(solvedOperations, key=lambda x: (x.machine, x.startTime))
  for i in sortedSolvedOperations:
    jobIndex = i.jobIndex
    opeIndex = i.opeIndex
    machine = i.machine
    processingTime = i.processingTime
    startTime = i.startTime
    endTime = i.endTime
    newLine = f"({jobIndex},{opeIndex}): {machine} {processingTime} {startTime} {endTime}"
    appendLineOutput(newLine, solvedPath, addZero=False)
