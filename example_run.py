from reader import Reader

reader = Reader()
assignment = reader.from_json_file('./example_files/expression_example.json')

# assignemnt -> answer -> block -> lines -> equation -> expression -> command and children expression
print(assignment.answers[0].block.lines[0].expressions[0].command)