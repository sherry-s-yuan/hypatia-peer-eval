from app.reader import Reader
from app.assignment import Assignment
from app.answer import Answer

def test_read_json_file():
  reader = Reader()
  assignment = reader.from_json_file('./example_files/block_example.json')

def test_load_data():
  reader = Reader()
  api_response = reader.data_from_json('./example_files/block_example.json')


