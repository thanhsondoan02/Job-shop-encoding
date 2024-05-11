import os
import re
import sys


def extract_time(file_path):
  with open(file_path, 'r') as file:
    content = file.read()
    match = re.search(r'Time taken: (\d+.\d+) seconds', content)
    if match:
      return float(match.group(1))
    else:
      return None

# argument 1: problem name
problemName = sys.argv[1]

problemDir = f'./{problemName}'

# get list of sorted makespan. Ex: [268, 531, 532, 596, 597]
makespans = [d for d in os.listdir(problemDir) if os.path.isdir(
    os.path.join(problemDir, d)) and d.startswith('L')]
makespans = [int(d[1:]) for d in makespans if d != 'L0']
makespans = sorted(makespans)

for makespan in makespans:
  makespanDir = f'{problemDir}/L{makespan}'
  repeats = [d for d in os.listdir(makespanDir)
             if os.path.isdir(os.path.join(makespanDir, d))]
  pTimes = []
  for repeat in repeats:
    repeatDir = f'{makespanDir}/{repeat}'
    files = os.listdir(repeatDir)
    if len(files) == 0: continue
    decodedFile = [i for i in files if "decoded" in i][0]
    pTimes.append(extract_time(f"{repeatDir}/{decodedFile}"))
  line = ""
  line += str(makespan)
  for pTime in pTimes:
    line += " " + str(pTime)
  print(line)
