from app.expression import Expression


class Equation:
  def __init__(self, raw_expression, expressions=[]):
    self.raw_expression = raw_expression
    self.expressions = expressions

  @classmethod
  def from_json(cls, raw_expression):
    expressions = []
    for exp in raw_expression:
      expressions.append(Expression.from_json(exp))
    return Equation(raw_expression, expressions)
