from app.answer import Answer
import random


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

    def answer_of_problem(self, problem) -> [Answer]:
        result = []
        for answer in self.answers:
            if answer.problem == problem:
                result.append(answer)
        return result

    def to_json(self, problem: int):
        answers = self.answer_of_problem(problem)
        if answers == []:
            return None
        result = []
        for answer in answers:
            json_obj = {
                'docid': self.docid,
                'docname': self.docname,
                'userid': self.userid,
                'username': self.username}
            json_obj.update(answer.to_json())
            result.append(json_obj)
        return result

    def find_exp_with_id(self, id: str):
        for answer in self.answers:
            exp = answer.find_exp_with_id(id)
            if exp is not None: return exp
        return None

    def find_answer_with_mathid(self, id):
        for answer in self.answers:
            if answer.mathid == id:
                return answer

    def __eq__(self, other):
        return self.docid == other.docid
