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


def isStartAfter(variable):
  return variable[0] == "S" and variable[1] == "a"


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


def stringToStartAfter(text):
  if not isStartAfter(text):
    raise Exception("Variable", text, "is not start after")
  numbers = [int(x) for x in text[3:-1].split(',')]
  return StartAfter(numbers[0], numbers[1], numbers[2])
