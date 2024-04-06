# Description: File processing functions for the project

# append line to end of file with 0 at the end
def appendLineOutput(line, outputPath, addZero=True):
  with open(outputPath, 'a') as f:
    if addZero:
      f.write(str(line) + ' 0\n')
    else:
      f.write(str(line) + '\n')


# add line to head of file
def addHeadFile(line, outputPath):
  # read current content
  with open(outputPath, 'r') as f:
    content = f.read()

  # add line to head of content and write to file
  with open(outputPath, 'w') as f:
    f.write(line + '\n' + content)


# delete all content of file
def clearFileContent(outputPath):
  with open(outputPath, 'w') as f:
    pass


def jobsFromFile(file_path):
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
