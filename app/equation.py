from app.expression import Expression
import random

class Equation:
    def __init__(self, raw_expression: dict, expressions: [Expression] = None):
        self.raw_expression = raw_expression
        self.expressions = expressions

    @classmethod
    def from_json(cls, raw_expression: dict):
        expressions = []
        for exp in raw_expression:
            expressions.append(Expression.from_json(exp))
        return Equation(raw_expression, expressions)

    def to_json(self):
        return [exp.to_json() for exp in self.expressions]

    def find_exp_with_id(self, id: str):
        for expression in self.expressions:
            exp = expression.find_exp_with_id(id)
            if exp is not None: return exp
        return None

    def generate_highlight_intercept(self):
        exp_ind = random.randrange(len(self.expressions))
        exp = self.expressions[exp_ind]
        return exp.generate_highlight_intercept()

