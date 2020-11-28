class Expression:
    def __init__(self, command: str, value: str, exp_id: str,
                 children: ['Expression']):
        self.command = command
        self.id = exp_id
        self.value = value
        self.children = children
        self.has_error = False
        self.err_type = None
        self.hint = None
        self.score = 0

    @classmethod
    def from_json(cls, exp: dict):
        command = exp['command'] if 'command' in exp else None
        exp_id = exp['id'] if 'id' in exp else None
        value = exp['value'] if 'value' in exp else None
        if 'children' not in exp:
            return Expression(command, value, exp_id, None)
        children = [Expression.from_json(child) for child in exp['children']]
        return Expression(command, value, exp_id, children)

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

    def add_error(self, error_type: str, hint: str):
        self.has_error = True
        self.err_type = error_type
        self.hint = hint

    def find_exp_with_id(self, id: str):
        if self.id == id:
            return self
        if self.children is None:
            return None
        for child_exp in self.children:
            exp = child_exp.find_exp_with_id(id)
            if exp is not None: return exp
        return None

    def subtree_contain_error(self) -> bool:
        """Check if this subtree contain error"""
        contain_error = self.has_error
        if self.children is None:
            return contain_error
        for child in self.children:
            contain_error = contain_error or child.subtree_contain_error()
        return contain_error

    def generate_highlight_intercept(self):
        # if there are only 1 more level below it, then generate this if it contain no error
        # if self.children is None or self.children[0].children is None:
        if not self.subtree_contain_error() and self.id is not None and self.command != '=':
            return self.id

    def get_difficulty_score(self):
        check = False
        weight_dict = {0: ["Plus", "Minus", "Multiply", "Divide", "ExpressionList", "Symbol", "Number", "="],
                       0.2: ["Root"],
                       0.4: ["Sum", "Product"],
                       0.6: ["TrigFunction"],
                       0.8: ["Exponent", "Log"],
                       1: ["Limit", "->", "Derivative", "Integral", "DefIntegral"]}
        for weight in weight_dict:
            if self.command in weight_dict[weight]:
                self.score += weight
                check = True
                break
        if not check:
            self.score += 1
        if self.children is None:
            return self.score
        else:
            for child in self.children:
                self.score += child.get_difficulty_score()
        return self.score
