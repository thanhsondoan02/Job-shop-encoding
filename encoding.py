from variables import *
from file_process import *
from utils import alarm
import os

def printJobs(jobs):
  for job in jobs:
    for operation in job:
      print("machine: ", operation[0], "time: ", operation[1])
    print("")


class Operation:
  def __init__(self, jobIndex, operationIndex, machine, processingTime):
    self.jobIndex = jobIndex
    self.operationIndex = operationIndex
    self.machine = machine
    self.processingTime = processingTime

  def __repr__(self):
    return f"Ope({self.jobIndex},{self.operationIndex},{self.machine}, {self.processingTime})"


variables = {}
count = 0


def resetVarAndCount():
  global variables, count
  variables = {}
  count = 0


def variableIndex(precedes):
  global count
  if precedes not in variables:
    count += 1
    variables[precedes] = count
  return variables[precedes]


def writeVariables(variablesPath):
  with open(variablesPath, 'w') as f:
    for key, value in variables.items():
      f.write(f'{key} {value}\n')


def encoding(inputPath, outputPath, variablesPath, L):
  clearFileContent(outputPath)
  resetVarAndCount()

  _, _, jobs = jobsFromFile(inputPath)
  machineOperations = {}

  for jobIndex, job in enumerate(jobs):
    for opeIndex, operation in enumerate(job):
      machine, time = operation

      # condition 1: precedes in same job
      if opeIndex != len(job) - 1:
        appendLineOutput(
            variableIndex(Precedes(jobIndex, opeIndex, jobIndex, opeIndex+1)),
            outputPath
        )

      # add to machineOperations for condition 2
      if machine not in machineOperations:
        machineOperations[machine] = []
      machineOperations[machine].append(
          Operation(jobIndex, opeIndex, machine, time))

  # condition 2: precedes in same machine
  # value: array of all operations in machine key
  for key, value in machineOperations.items():
    for i in range(0, len(value)-1):
      for j in range(i+1, len(value)):
        var1 = variableIndex(
            Precedes(value[i].jobIndex, value[i].operationIndex,
                     value[j].jobIndex, value[j].operationIndex)
        )
        var2 = variableIndex(
            Precedes(value[j].jobIndex, value[j].operationIndex,
                     value[i].jobIndex, value[i].operationIndex)
        )
        appendLineOutput(f'{var1} {var2}', outputPath)

  # for show progress
  running = 0
  maxRunning = len(jobs) * len(jobs[0])

  for jobIndex, job in enumerate(jobs):
    for opeIndex, operation in enumerate(job):

      # condition 3: start after
      t1 = sum(job[i][1] for i in range(0, opeIndex))
      appendLineOutput(
          variableIndex(StartAfter(jobIndex, opeIndex, t1)),
          outputPath
      )

      # condition 4: end before
      t2 = L - sum(job[i][1] for i in range(opeIndex+1, len(job)))
      appendLineOutput(
          variableIndex(EndBefore(jobIndex, opeIndex, t2)),
          outputPath
      )

      # condition 5: start after t -> start after t-1
      for t in range(1, L+1):
        var1 = variableIndex(StartAfter(jobIndex, opeIndex, t))
        var2 = variableIndex(StartAfter(jobIndex, opeIndex, t-1))
        appendLineOutput(f'-{var1} {var2}', outputPath)

      # condition 6: end before t -> end before t+1
      for t in range(0, L):
        var1 = variableIndex(EndBefore(jobIndex, opeIndex, t))
        var2 = variableIndex(EndBefore(jobIndex, opeIndex, t+1))
        appendLineOutput(f'-{var1} {var2}', outputPath)

      processingTime = operation[1]

      # condition 7: start after -> not end before:
      for t in range(0, L-processingTime+2):
        var1 = variableIndex(StartAfter(jobIndex, opeIndex, t))
        var2 = variableIndex(EndBefore(jobIndex, opeIndex, t+processingTime-1))
        appendLineOutput(f'-{var1} -{var2}', outputPath)

      # condition 8: start after + precedes
      precedes_list = [key for key in variables.keys()
                       if isinstance(key, Precedes)
                       and key.jobIndex1 == jobIndex and key.opeIndex1 == opeIndex]
      for t in range(0, L-processingTime+1):
        for precedes in precedes_list:
          var1 = variableIndex(StartAfter(jobIndex, opeIndex, t))
          var2 = variableIndex(precedes)
          var3 = variableIndex(
              StartAfter(precedes.jobIndex2, precedes.opeIndex2, t+processingTime))
          appendLineOutput(f'-{var1} -{var2} {var3}', outputPath)

      # show progress
      running += 1
      percent = running * 1.0 / maxRunning * 100
      print(f"Running {percent:.2f}%")

  with open(outputPath, 'r') as file:
    lines = file.readlines()

  addHeadFile(f"p cnf {len(variables)} {len(lines)}", outputPath)
  writeVariables(variablesPath)
  alarm()

problem = "mine"
for i in range(11, 15):
  outputFileName = f"{problem}_L{i}_encoded.cnf"
  variableFileName = f"{problem}_L{i}_variables.txt"
  print(f"Start encoding {problem} L{i}")
  folderPath = f"./{problem}/L{i}"
  if not os.path.exists(folderPath):
    os.makedirs(folderPath)
  encoding(f"./{problem}/{problem}.txt",
           f"./{problem}/L{i}/{outputFileName}",
           f"./{problem}/L{i}/{variableFileName}",
           L=i)
