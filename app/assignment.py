from app.answer import Answer


class Assignment:
    answers: [Answer]
    student_id: int

    def __init__(self, docid: str, docname: str, userid: int, username: str):
        self.docid = docid
        self.docname = docname
        self.userid = userid
        self.username = username
        self.answers = []

    def add_answer(self, answer: Answer):
        self.answers.append(answer)
