# a builder
import json
from app.assignment import Assignment
from app.answer import Answer


class Reader:
    def from_json_file(self, fn: str):
        with open(fn) as f:
            data = json.load(f)
        print('API response data: ', data)
        return self.from_json_stream(data)

    def data_from_json(self, fn):
        with open(fn) as f:
            return json.load(f)

    @staticmethod
    def from_json_stream(data: dict):
        docid = data['docid']
        docname = data['docname']
        userid = data['userid']
        username = data['username']
        assignment = Assignment(docid, docname, userid, username)
        mathid = data['mathid']
        version = data['version']
        problem = data['problem']
        expression = data['value']
        answer = Answer.from_json(mathid, version, problem, expression)
        assignment.add_answer(answer)
        return assignment
