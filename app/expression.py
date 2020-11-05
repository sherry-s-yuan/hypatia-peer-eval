class Expression:
    def __init__(self, command: str, value: str, id: str, children: ['Expression']):
        self.command = command
        self.id = id
        self.value = value
        self.children = children
        self.error = False
        self.hint = None

    @classmethod
    def from_json(cls, exp: 'Expression'):
        command = exp['command'] if 'command' in exp else None
        id = exp['id'] if 'id' in exp else None
        value = exp['value'] if 'value' in exp else None
        if 'children' not in exp:
            return Expression(command, value, id, None)
        children = [Expression.from_json(child) for child in exp['children']]
        return Expression(command, value, id, children)

    def to_json(self):
      json_obj = {}
      if self.command is not None:
        json_obj["command"] = self.command
      if self.value is not None:
        json_obj["value"] = self.value
      if self.id is not None:
        json_obj["id"] = self.id

      if self.children is None:
        return json_obj
      json_obj["children"] = [child.to_json() for child in self.children]
      return json_obj

    def has_error(self, hint):
        self.error = True
        self.hint = hint
