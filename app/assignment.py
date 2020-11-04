from app.answer import Answer


class Assignment:
    questions: [Answer]
    student_id: int

    def __init__(self, docid, docname, userid, username):
        self.docid = docid
        self.docname = docname
        self.userid = userid
        self.username = username
        self.answers = []

    def add_answer(self, answer: Answer):
        self.answers.append(answer)
