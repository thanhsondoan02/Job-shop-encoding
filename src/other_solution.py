from variables import *
from file_process import *
from sum_up_solution import sumUpSolutions
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
      print(f"Encoding {percent:.2f}%")

  with open(outputPath, 'r') as file:
    lines = file.readlines()

  addHeadFile(f"p cnf {len(variables)} {len(lines)}", outputPath)
  writeVariables(variablesPath)


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


def count_folders(directory):
  return len([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))])


def incrementLastNumOfFirstLine(file_path):
  with open(file_path, 'r') as file:
    lines = file.readlines()

  numbers = lines[0].split()
  numbers[-1] = str(int(numbers[-1]) + 1)
  lines[0] = ' '.join(numbers) + '\n'

  with open(file_path, 'w') as file:
    file.writelines(lines)


def addNegativePreviousSolutions(root, encodedFilePath):
  count = count_folders(root)
  for solutionIndex in range(count-1):
    solutionDir = f"{root}/solution{solutionIndex}"
    files = os.listdir(solutionDir)
    resultFile = [i for i in files if "result" in i][0]
    with open(f"{solutionDir}/{resultFile}", 'r') as file:
      lines = file.readlines()
      if len(lines) > 1:
        variables = lines[1].split()
        negated_variables = [-int(var) for var in variables]
        with open(encodedFilePath, 'a') as file:
          file.write(' '.join(map(str, negated_variables)) + '\n')
        incrementLastNumOfFirstLine(encodedFilePath)
      else:
        raise Exception("No second line in the file")


# argument 1: problem name
# argument 2: makespan
# argument 3: limit time
problem = sys.argv[1]
makespan = int(sys.argv[2])
limitTime = int(sys.argv[3])

while True:
  start_time = time.time()

  i = makespan
  inputPath = f"./{problem}/{problem}.txt"

  root = f"./{problem}/L{i}/solutions"
  if not os.path.exists(root):
    os.makedirs(root)

  folderPath = f"{root}/solution{count_folders(root)}"
  if not os.path.exists(folderPath):
    os.makedirs(folderPath)

  encodedFilePath = f"{folderPath}/{problem}_L{i}_encoded.cnf"
  variablePath = f"{folderPath}/{problem}_L{i}_variables.txt"
  resultFilePath = f"{folderPath}/{problem}_L{i}_result.txt"
  terminalFilePath = f"{folderPath}/{problem}_L{i}_terminal.txt"
  decodedFilePath = f"{folderPath}/{problem}_L{i}_decoded.txt"

  # Using encoded file from first solution if possible
  if count_folders(root) == 1:
    print(f"Start encoding {problem} L{i}")
    encoding(inputPath, encodedFilePath, variablePath, L=i)
  else:
    copy_file(f'{root}/solution0/{problem}_L{i}_encoded.cnf', encodedFilePath)
    copy_file(f'{root}/solution0/{problem}_L{i}_variables.txt', variablePath)

  addNegativePreviousSolutions(root, encodedFilePath)

  # run minisat solver
  print(f"Running minisat solver for {problem} L{i}...")
  command = f"..\.\minisat.exe {encodedFilePath} {resultFilePath}"
  result = subprocess.run(
      command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout = result.stdout.decode()
  stderr = result.stderr.decode()
  with open(terminalFilePath, 'w') as f:
    f.write(stderr.replace('\n', ''))

  # run decoder
  print(f"Running decoder for {problem} L{i}...")
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
  print(f"Done {problem} L{i} in {time_taken} seconds\n")

  # check if UNSAT stop
  with open(resultFilePath, 'r') as file:
    first_line = file.readline().strip()
  if first_line != "SAT":
    break

  # if exceed time limit stop
  limitTime -= time_taken
  if limitTime < 0:
    break

sumUpSolutions(problem, makespan)
