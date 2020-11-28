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
        highest_score = 0
        equal_bool = False
        highest_score_expression = self.expressions[-1]
        for ex in self.expressions:
            if ex.command == "=":
                equal_bool = True
            if equal_bool:
                difficulty_score = ex.get_difficulty_score()
                if difficulty_score > highest_score:
                    highest_score = difficulty_score
                    highest_score_expression = ex
        return highest_score_expression.generate_highlight_intercept()

    def get_difficulty_score(self):
        score = 0
        for exp in self.expressions:
            score += exp.get_difficulty_score()
        return score

    def contains_error(self):
        for exp in self.expressions:
            if exp.subtree_contain_error():
                return True
        return False
