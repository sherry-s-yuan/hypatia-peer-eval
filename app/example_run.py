from app.reader import Reader

reader = Reader()
assignment = reader.from_json_file('../example_files/block_example.json')

api_response = reader.data_from_json('../example_files/block_example.json')
reconstructed_response = assignment.to_json(2)
print(api_response == reconstructed_response)

# assignment -> answer -> lines -> equation -> expression ->

# convert answer to question 2 back to json
print('Reconstructed data:', assignment.to_json(2))
print()

# print the first line's first expression json
print("First line's first expression: ",
      assignment.answers[0].lines[0].expressions[0].to_json())
print()

# print first line's json
print("First line's expression", assignment.answers[0].lines[0].to_json())
print()

# print 0-th index answer's json
print(assignment.answers[0].to_json())
print()
