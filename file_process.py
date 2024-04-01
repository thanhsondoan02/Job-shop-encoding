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
