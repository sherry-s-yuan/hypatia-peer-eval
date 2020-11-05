# a builder
import json
from app.assignment import Assignment
from app.answer import Answer


class Reader:
    def from_json_file(self, fn):
        with open(fn) as f:
            data = json.load(f)
        return self.from_json_stream(data)

    @staticmethod
    def from_json_stream(self, data):
        print(type(data))
        docid = data['docid']
        docname = data['docname']
        userid = data['userid']
        username = data['username']
        assignment = Assignment(docid, docname, userid, username)
        mathid = data['mathid']
        version = data['version']
        problem = data['problem']
        expression = data['value']
        answer = Answer(mathid, version, problem, expression)
        assignment.add_answer(answer)
        return assignment
