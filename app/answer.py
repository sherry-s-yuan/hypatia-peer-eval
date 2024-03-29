from app.equation import Equation


class Answer:
    def __init__(self, mathid: str, version: int, problem: int, raw_lines: [],
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
        json_obj = {}
        json_obj['mathid'] = self.mathid
        json_obj['version'] = self.version
        json_obj['problem'] = self.problem
        if self.lines is not None:
            json_obj['value'] = [line.to_json() for line in self.lines]
        return json_obj

    def find_exp_with_id(self, id: str):
        for line in self.lines:
            exp = line.find_exp_with_id(id)
            if exp is not None: return exp
        return None

    def generate_highlight_intercept(self):
        highest_score = 0
        highest_score_equation = self.lines[0]
        for eq in self.lines:
            difficulty_score = eq.get_difficulty_score()
            if difficulty_score > highest_score:
                highest_score = difficulty_score
                highest_score_equation = eq
            elif difficulty_score == highest_score:
                if highest_score_equation.contains_error():
                    highest_score_equation = eq
        generated_id = highest_score_equation.generate_highlight_intercept()
        if generated_id:
            return generated_id
        else:
            pass  # regenerate again?

