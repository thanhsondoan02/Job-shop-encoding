
def jobsFromFile(file_path="input.txt"):
  jobs = []
  with open(file_path, "r") as file:
    jobs_count, operations_count = file.readline().strip().split()
    jobs_count = int(jobs_count)
    operations_count = int(operations_count)
    for i in range(jobs_count):
      job = []
      line = file.readline().strip().split()
      for j in range(0, operations_count):
        job.append((int(line[j*2]), int(line[j*2+1])))
      jobs.append(job)
  return jobs_count, operations_count, jobs


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


class Precedes:
  def __init__(self, jobIndex1, opeIndex1, jobIndex2, opeIndex2):
    self.jobIndex1 = jobIndex1
    self.opeIndex1 = opeIndex1
    self.jobIndex2 = jobIndex2
    self.opeIndex2 = opeIndex2

  def __hash__(self):
    return hash((self.jobIndex1, self.opeIndex1, self.jobIndex2, self.opeIndex2))

  def __eq__(self, other):
    if isinstance(other, Precedes):
      return (self.jobIndex1 == other.jobIndex1 and self.opeIndex1 == other.opeIndex1
              and self.jobIndex2 == other.jobIndex2 and self.opeIndex2 == other.opeIndex2)
    return False

  def __str__(self):
    return f"Pr({self.jobIndex1},{self.opeIndex1},{self.jobIndex2},{self.opeIndex2})"

  def __repr__(self):
    return f"Pr({self.jobIndex1},{self.opeIndex1},{self.jobIndex2},{self.opeIndex2})"


class StartAfter:
  def __init__(self, jobIndex, opeIndex, time):
    self.jobIndex = jobIndex
    self.opeIndex = opeIndex
    self.time = time

  def __hash__(self):
    return hash((self.jobIndex, self.opeIndex, self.time))

  def __eq__(self, other):
    if isinstance(other, StartAfter):
      return (self.jobIndex == other.jobIndex and self.opeIndex == other.opeIndex
              and self.time == other.time)
    return False

  def __repr__(self) -> str:
    return f"Sa({self.jobIndex},{self.opeIndex},{self.time})"


class EndBefore:
  def __init__(self, jobIndex, opeIndex, time):
    self.jobIndex = jobIndex
    self.opeIndex = opeIndex
    self.time = time

  def __hash__(self):
    return hash((self.jobIndex, self.opeIndex, self.time))

  def __eq__(self, other):
    if isinstance(other, EndBefore):
      return (self.jobIndex == other.jobIndex and self.opeIndex == other.opeIndex
              and self.time == other.time)
    return False

  def __repr__(self) -> str:
    return f"Eb({self.jobIndex},{self.opeIndex},{self.time})"


variables = {}
count = 0
L = 1096


def variableIndex(precedes):
  global count
  if precedes not in variables:
    count += 1
    variables[precedes] = count
  return variables[precedes]


def writeVariables():
  with open('variables.txt', 'w') as f:
    for key, value in variables.items():
      f.write(f'{key} {value}\n')


def deleteOutput():
  with open('output.txt', 'w') as f:
    pass


def appendLineOutput(line):
  with open('output.txt', 'a') as f:
    f.write(str(line) + ' 0 \n')


deleteOutput()
jobs_count, operations_count, jobs = jobsFromFile()
machineOperations = {}

for jobIndex, job in enumerate(jobs):
  for opeIndex, operation in enumerate(job):
    machine, time = operation

    # condition 1: precedes
    if opeIndex != len(job) - 1:
      appendLineOutput(
          variableIndex(Precedes(jobIndex, opeIndex, jobIndex, opeIndex+1))
      )

    # add to machineOperations for condition 2
    if machine not in machineOperations:
      machineOperations[machine] = []
    machineOperations[machine].append(
        Operation(jobIndex, opeIndex, machine, time))

# condition 2: same machine
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
      appendLineOutput(f'{var1} {var2}')

for jobIndex, job in enumerate(jobs):
  for opeIndex, operation in enumerate(job):
    # condition 3: start after
    t1 = sum(job[i][1] for i in range(0, opeIndex))
    appendLineOutput(
        variableIndex(StartAfter(jobIndex, opeIndex, t1))
    )
    # condition 4: end before
    t2 = L - sum(job[i][1] for i in range(opeIndex+1, len(job)))
    appendLineOutput(
        variableIndex(EndBefore(jobIndex, opeIndex, t2))
    )

for jobIndex, job in enumerate(jobs):
  for opeIndex, operation in enumerate(job):
    # condition 5: start after t -> start after t-1
    for t in range(1, L+1):
      var1 = variableIndex(StartAfter(jobIndex, opeIndex, t))
      var2 = variableIndex(StartAfter(jobIndex, opeIndex, t-1))
      appendLineOutput(f'-{var1} {var2}')

    # condition 6: end before t -> end before t+1
    for t in range(0, L):
      var1 = variableIndex(EndBefore(jobIndex, opeIndex, t))
      var2 = variableIndex(EndBefore(jobIndex, opeIndex, t+1))
      appendLineOutput(f'-{var1} {var2}')

    processingTime = operation[1]

    # condition 7: start after -> not end before:
    for t in range(0, L-processingTime+1):
      var1 = variableIndex(StartAfter(jobIndex, opeIndex, t))
      var2 = variableIndex(EndBefore(jobIndex, opeIndex, t+processingTime-1))
      appendLineOutput(f'-{var1} -{var2}')

    # condition 8:
    precedes_list = [key for key in variables.keys()
                     if isinstance(key, Precedes)
                     and key.jobIndex1 == jobIndex and key.opeIndex1 == opeIndex]
    for t in range(0, L-processingTime+1):
      for precedes in precedes_list:
        var1 = variableIndex(StartAfter(jobIndex, opeIndex, t))
        var2 = variableIndex(precedes)
        var3 = variableIndex(
            StartAfter(precedes.jobIndex2, precedes.opeIndex2, t+processingTime))
        appendLineOutput(f'-{var1} -{var2} {var3}')

writeVariables()
