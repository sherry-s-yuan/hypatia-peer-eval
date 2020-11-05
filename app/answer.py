from app.equation import Equation


class Answer:
    def __init__(self, mathid: str, version: int, problem: int, raw_lines: dict,
                 lines: [Equation] = None):
        self.mathid = mathid
        self.version = version
        self.problem = problem
        self.raw_lines = raw_lines
        self.lines = lines

    @classmethod
    def from_json(cls, mathid: str, version: int, problem: int,
                  raw_lines: dict):
        lines = []
        for line in raw_lines:
            lines.append(Equation.from_json(line))
        return Answer(mathid, version, problem, raw_lines, lines)

    def to_json(self):
        json_obj = {
            'mathid': self.mathid,
            'version': self.version,
            'problem': self.problem,
            'value': [line.to_json() for line in self.lines]}
        return json_obj
