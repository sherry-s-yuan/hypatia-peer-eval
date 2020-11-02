class Question:
    question_id: int
    answer: bool

    def __init__(self, question_id: int, answer: bool):
        self.question_id = question_id
        self.answer = answer
