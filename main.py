
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
  return jobs


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


class StartAfter:
  def __init__(self, jobIndex, opeIndex, time):
    self.jobIndex = jobIndex
    self.opeIndex = opeIndex
    self.time = time

  def __hash__(self):
    return hash((self.jobIndex, self.opeIndex, self.time))

  def __eq__(self, other):
    if isinstance(other, StartAfter):
      return (self.jobIndex == other.jobIndex and self.opeIndex == other.opeIndex and self.time == other.time)
    return False


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


variables = {}
count = 0
L = 1096


def variableIndex(precedes):
  global count
  if precedes not in variables:
    count += 1
    variables[precedes] = count
  return variables[precedes]


def deleteOutput():
  with open('output.txt', 'w') as f:
    pass


def appendLineOutput(line):
  with open('output.txt', 'a') as f:
    f.write(line + '\n')


deleteOutput()
jobs = jobsFromFile()

for job in jobs:
  for operation in job:
    print("machine: ", operation[0], "time: ", operation[1])
  print("")