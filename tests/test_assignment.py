from app.reader import Reader
from app.assignment import Assignment
from app.answer import Answer

def test_to_json():
  reader = Reader()
  assignment = reader.from_json_file('./example_files/block_example.json')
  api_response = reader.data_from_json('./example_files/block_example.json')
  reconstructed_response = assignment.to_json(2)
  assert api_response == reconstructed_response

def test_add_answer():
  assignment = Assignment('docid', 'docname', 2314, 'username')
  answer1 = Answer('1', 4, 2, {}, None)
  answer2 = Answer('2', 4, 2, {}, None)
  answer3 = Answer('1', 4, 2, {}, None)
  assignment.add_answer(answer1)
  assignment.add_answer(answer2)
  assert len(assignment.answers) == 2
  assignment.add_answer(answer3)
  assert len(assignment.answers) == 2


