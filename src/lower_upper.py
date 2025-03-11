import sys
import subprocess
from file_process import jobsFromFile

# argument 1: problem name
problem = sys.argv[1]

problemPath = f"./{problem}/{problem}.txt"


upperBound = 0
job_count, operation_count, jobs = jobsFromFile(problemPath)



result = subprocess.run(
    ["python", "encoding.py", "1"], capture_output=True)
last_line = result.stdout

# write result to outputPath

