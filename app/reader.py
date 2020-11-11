# a builder
import json
from app.assignment import Assignment
from app.answer import Answer


class Reader:
    def __init__(self):
        self.assignments = []

    def assignment_from_json_file(self, fn: str):
        with open(fn) as f:
            data = json.load(f)
        print('API response data: ', data)
        return self.assignment_from_json_stream(data)

    def data_from_json(self, fn):
        with open(fn) as f:
            return json.load(f)

    def assignment_from_json_stream(self, data: dict):
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
        self.add_assignment(assignment, answer)
        return assignment

    def add_assignment(self, assignment: Assignment, answer: Answer):
        # add new assignment if does not exist
        # otherwise update answer in existing assignment
        ass_with_same_id = self.find_assign_with_id(assignment.docid)
        if ass_with_same_id is None:
            self.assignments.append(assignment)
        else:
            ass_with_same_id.add_answer(answer)

    def find_assign_with_id(self, docid) -> Assignment:
        '''return assignment object with the same given docid'''
        for a in self.assignments:
            if a.docid == docid:
                return a

    def add_error(self, docid: str, problem_num: int, command_id: str, error_type: str, hint: str):
        ass = self.find_assign_with_id(docid)
        ans = ass.answer_of_problem(problem_num)
        exp = None
        for a in ans:
            exp = a.find_exp_with_id(command_id)
            if exp: break
        if exp is None:
            print("Cannot find expression with this error")
            return
        exp.add_error(error_type, hint)

