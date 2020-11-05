from app.equation import Equation


class Answer:
    def __init__(self, mathid: str, version: int, problem: int, raw_lines: dict, lines: [Equation] = None):
        self.mathid = mathid
        self.version = version
        self.problem = problem
        self.raw_lines = raw_lines
        self.lines = lines

    @classmethod
    def from_json(cls, mathid: str, version: int, problem: int, raw_lines: dict):
        lines = []
        for line in raw_lines:
            lines.append(Equation.from_json(line))
        return Answer(mathid, version, problem, raw_lines, lines)

    def to_json(self):
        json_obj = {}
        json_obj['mathid'] = self.mathid
        json_obj['version'] = self.version
        json_obj['problem'] = self.problem
        if self.lines is not None:
            json_obj['value'] = [line.to_json() for line in self.lines]
        return json_obj