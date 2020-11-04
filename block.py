from equation import Equation

class Block:
  def __init__(self, raw_lines, lines=[]):
    self.raw_lines = raw_lines
    self.lines = lines

  @classmethod
  def from_json(cls, raw_lines):
    lines = []
    for line in raw_lines:
      lines.append(Equation.from_json(line))
    return Block(raw_lines, lines)




