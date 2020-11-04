

class Expression:
  def __init__(self, command, id, children=[]):
    self.command = command
    self.id = id
    self.children = children
    self.error = False
    self.hint = None

  @classmethod
  def from_json(cls, exp):
    if 'children' not in exp:
      return Expression(exp['command'], exp['id'])
    return Expression(exp['command'], exp['id'], exp['children'])

  def has_error(self, hint):
    self.error = True
    self.hint = hint


