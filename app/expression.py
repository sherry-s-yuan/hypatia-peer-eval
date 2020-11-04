

class Expression:
  def __init__(self, command: str, id: str, children:['Expression']=[]):
    self.command = command
    self.id = id
    self.children = children
    self.error = False
    self.hint = None

  @classmethod
  def from_json(cls, exp:'Expression'):
    if 'children' not in exp:
      return Expression(exp['command'], exp['id'] if 'id' in exp else None)
    children = [Expression.from_json(child) for child in exp['children']]
    return Expression(exp['command'], exp['id'] if 'id' in exp else None, children)

  def has_error(self, hint):
    self.error = True
    self.hint = hint


