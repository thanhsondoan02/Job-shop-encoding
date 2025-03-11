import pygame


def alarm():
  pygame.mixer.init()
  pygame.mixer.music.load("./alarm.mp3")
  pygame.mixer.music.play()


def verifyOperationSameJob(opeString1, opeString2, makespan):
  ope1 = opeString1.split(' ')
  ope2 = opeString2.split(' ')
  ope1 = [int(i) for i in ope1]
  ope2 = [int(i) for i in ope2]

  job1 = ope1[0]
  endTime1 = ope1[5]

  job2 = ope2[0]
  startTime2 = ope2[4]
  endTime2 = ope2[5]

  if endTime1 > makespan or endTime2 > makespan:
    return False

  if job1 != job2:
    return True
  else:
    return endTime1 <= startTime2


def verifyOperationSameMachine(opeString1, opeString2, makespan):
  ope1 = opeString1.split(' ')
  ope2 = opeString2.split(' ')
  ope1 = [int(i) for i in ope1]
  ope2 = [int(i) for i in ope2]

  machine1 = ope1[2]
  endTime1 = ope1[5]

  machine2 = ope2[2]
  startTime2 = ope2[4]
  endTime2 = ope2[5]

  if endTime1 > makespan or endTime2 > makespan:
    return False

  if machine1 != machine2:
    return True
  else:
    return endTime1 <= startTime2


def calMakespan(decodedFileDir):
  dirs = decodedFileDir.split('_')
  texts = [i.replace('L', '') for i in dirs if 'L' in i]
  makespan = texts[len(texts)-1]
  return int(makespan)


def verify_schedule(decodedFileDir):
  makespan = calMakespan(decodedFileDir)

  with open(decodedFileDir, 'r') as file:
    lines = file.readlines()
    lines = lines[:-1]
    lines = [i.replace('\n', '').replace('(', '').replace(',', ' ')
             .replace(')', '').replace(':', '')
             for i in lines if i != '\n']
  for i in range(len(lines)//2-1):
    if not verifyOperationSameJob(lines[i], lines[i+1], makespan):
      return False
  for i in range(len(lines)//2, len(lines)-1):
    if not verifyOperationSameMachine(lines[i], lines[i+1], makespan):
      return False
  return True


# print(verify_schedule(
#     "D:\EncodingJSSP\orb07\L397\solutions\solution0\orb07_L397_decoded.txt"))
