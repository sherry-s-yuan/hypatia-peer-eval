from app.block import Block

class Answer:
  def __init__(self, mathid, version, problem, block):
    self.mathid = mathid
    self.version = version
    self.problem = problem
    self.block = Block.from_json(block)
