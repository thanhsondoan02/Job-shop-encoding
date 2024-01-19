
def readFile(file_path = "input.txt"):
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

printJobs(readFile())