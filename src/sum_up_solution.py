import os
import re
import sys
from utils import verify_schedule


def extract_time(file_path):
  with open(file_path, 'r') as file:
    content = file.read()

    # if not satisfiable, return None
    lineCount = content.count('\n') + 1
    if lineCount < 4:
      return None

    # If no time found, return None
    match = re.search(r'Time taken: (\d+.\d+) seconds', content)
    if match:
      return float(match.group(1))
    else:
      return None


def sumUpSolutions(problemName, makespan):
  solutionsDir = f'./{problemName}/L{makespan}/solutions'
  solutions = [d for d in os.listdir(solutionsDir)
               if os.path.isdir(os.path.join(solutionsDir, d)) and 'solution' in d and 'solution0' not in d]
  solutions = sorted(solutions, key=lambda s: int(s.replace('solution', '')))

  assignments = []
  # schedules = []
  mapSchedules = {}

  for solution in solutions:
    solutionDir = f'{solutionsDir}/{solution}'

    files = os.listdir(solutionDir)
    if len(files) == 0:
      continue

    decodedFileList = [i for i in files if "decoded" in i]
    if len(decodedFileList) == 0:
      continue

    resultFileList = [i for i in files if "result" in i]
    if len(resultFileList) == 0:
      continue

    decodedFile = decodedFileList[0]
    decodedFileDir = f"{solutionDir}/{decodedFile}"

    # print processing time for each solution
    processingTime = extract_time(decodedFileDir)
    if processingTime == None:  # if not sat or no time found
      continue
    print(solution + " " + str(processingTime))

    # add assignment and schedules
    if not verify_schedule(decodedFileDir):
      continue
    with open(decodedFileDir, 'r') as file:
      lines = file.readlines()[:-2]
      schedule = ''.join(lines)
      # schedules.append(schedule)
      if schedule not in mapSchedules:
        mapSchedules[schedule] = solution

    resultFile = resultFileList[0]
    resultFileDir = f"{solutionDir}/{resultFile}"
    with open(resultFileDir, 'r') as file:
      assignment = file.readlines()[1]
      assignments.append(assignment)

  # setSchedules = set(schedules)
  print(
      f"Total {len(set(assignments))} assignments, {len(mapSchedules.keys())} different schedules.")

  indicesString = "First folder of different schedules:"
  for schedule in mapSchedules.keys():
    indicesString += " " + str(mapSchedules[schedule])
  print(indicesString)


# # argument 1: problem name
# # argument 2: makespan
# problem = sys.argv[1]
# makespan = int(sys.argv[2])
# sumUpSolutions(problem, makespan)
