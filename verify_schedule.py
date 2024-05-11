import os


def getMatrixSchedule(fileDir):
  matrix = []
  with open(fileDir, 'r') as file:
    lines = file.readlines()
    lines = [i.replace('\n', '').replace('(', '').replace(')', '').replace(':', '').replace(',', ' ')
             for i in lines if i != '\n' and '(' in i]
    for line in lines:
      ope = line.split(' ')
      ope = [int(i) for i in ope]
      matrix.append(ope)
  return matrix


def getMakespan(fileDir):
  dirs = fileDir.split('\\')
  fileName = dirs[-1]
  makeSpan = fileName.split('_')[1].replace('L', '')
  return int(makeSpan)


def verifySchedule(fileDir):
  makespan = getMakespan(fileDir)
  matrix = getMatrixSchedule(fileDir)
  for i in range(len(matrix)//2):
    line = matrix[i]
    endTime = line[5]
    if endTime > makespan:
      return False

    if i != len(matrix)//2 - 1:
      nextLine = matrix[i+1]
      startTimeNextLine = nextLine[4]
      jobIndex = line[0]
      jobIndexNextLine = nextLine[0]
      if jobIndex == jobIndexNextLine and endTime > startTimeNextLine:
        return False

  for i in range(len(matrix)//2, len(matrix)):
    line = matrix[i]
    endTime = line[5]
    if endTime > makespan:
      return False

    if i != len(matrix) - 1:
      nextLine = matrix[i+1]
      startTimeNextLine = nextLine[4]
      machine = line[2]
      machineNextLine = nextLine[2]
      if machine == machineNextLine and endTime > startTimeNextLine:
        return False

  return True


# print(verifySchedule(
#     'D:\EncodingJSSP\mine\L12\solutions\solution0\mine_L12_decoded.txt'))

solutions = os.listdir('./mine/L12/solutions')
scheduleDirs = []
for solution in solutions:
  filesInSolutionDir = os.listdir(f'./mine/L12/solutions/{solution}')
  if 'mine_L12_decoded.txt' in filesInSolutionDir:
    scheduleDirs.append(
        f'./mine/L12/solutions/{solution}/mine_L12_decoded.txt')

results = [verifySchedule(v) for v in scheduleDirs]
if False in results:
  print("Bad")
else:
  print("Good")
  
