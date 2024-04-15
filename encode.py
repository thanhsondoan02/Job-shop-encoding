from variables import *
from file_process import *
from utils import alarm
import os
import sys
import subprocess
import time


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


def variableIndex(inputVar):
  global count
  if inputVar not in variables:
    count += 1
    variables[inputVar] = count
  return variables[inputVar]


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


def lowerUpper(inputPath):
  minTime = None
  for key in variables.keys():
    if isinstance(key, StartAfter):
      if minTime is None or key.time < minTime:
        minTime = key.time
    if isinstance(key, EndBefore):
      if minTime is None or key.time < minTime:
        minTime = key.time
  lowerBound = -minTime

  _, _, jobs = jobsFromFile(inputPath)
  upperBound = 0
  for job in jobs:
    for operation in job:
      upperBound += operation[1]

  lowerUpperFile = f"./{problem}/{problem}_lower_upper.txt"
  with open(lowerUpperFile, 'w') as f:
    f.write(f"LB = {lowerBound}, UB = {upperBound}")


# argument 1: problem name
# next arguments: list of L
problem = sys.argv[1]
makespan_list = []
for i in range(2, len(sys.argv)):
  makespan_list.append(int(sys.argv[i]))

for i in makespan_list:
  start_time = time.time()
  
  inputPath = f"./{problem}/{problem}.txt"
  folderPath = f"./{problem}/L{i}"
  encodedFilePath = f"{folderPath}/{problem}_L{i}_encoded.cnf"
  variablePath = f"{folderPath}/{problem}_L{i}_variables.txt"
  resultFilePath = f"{folderPath}/{problem}_L{i}_result.txt"
  terminalFilePath = f"{folderPath}/{problem}_L{i}_terminal.txt"
  decodedFilePath = f"{folderPath}/{problem}_L{i}_decoded.txt"

  if not os.path.exists(folderPath):
    os.makedirs(folderPath)

  print(f"Start encoding {problem} L{i}")
  encoding(inputPath, encodedFilePath, variablePath, L=i)
  if i == 0:
    lowerUpper(inputPath)
  else:
    # run minisat solver
    command = f"..\.\minisat.exe {encodedFilePath} {resultFilePath}"
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.stdout.decode()
    stderr = result.stderr.decode()
    with open(terminalFilePath, 'w') as f:
      f.write(stderr.replace('\n', ''))

    # run decoder
    with open(resultFilePath, 'r') as f:
      first_line = f.readline()
    if first_line == "SAT\n":
      command = f"python decode.py {variablePath} {resultFilePath} {decodedFilePath} {inputPath}"
      result = subprocess.run(
          command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # calculate CPU time for each L
    end_time = time.time()
    time_taken = end_time - start_time
    appendLineOutput(
        f"\nTime taken: {time_taken} seconds", decodedFilePath, addZero=False)
