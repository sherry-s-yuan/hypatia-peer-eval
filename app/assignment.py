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
        for i, a in enumerate(self.answers):
            if a.mathid == answer.mathid:
                self.answers[i] = answer
                return
        self.answers.append(answer)

    def answer_to_problem(self, problem):
        for answer in self.answers:
            if answer.problem == problem:
                return answer
        return None

    def to_json(self, problem: int):
        answer = self.answer_to_problem(problem)
        if answer is None:
            return None
        json_obj = {
            'docid': self.docid,
            'docname': self.docname,
            'userid': self.userid,
            'username': self.username}
        json_obj.update(answer.to_json())
        return json_obj
