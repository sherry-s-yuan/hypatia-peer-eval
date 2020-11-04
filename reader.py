# a builder
import json
from assignment import Assignment
from answer import Answer


class Reader:
  def from_json_file(self, fn):
    with open(fn) as f:
      data = json.load(f)
    return self.from_json_stream(data)

  def from_json_stream(self, data):
    print(type(data))
    docid = data['docid']
    docname = data['docname']
    userid = data['userid']
    username = data['username']
    assignemnt = Assignment(docid, docname, userid, username)
    mathid = data['mathid']
    version = data['version']
    problem = data['problem']
    expression = data['value']
    answer = Answer(mathid, version, problem, expression)
    assignemnt.add_answer(answer)
    return assignemnt