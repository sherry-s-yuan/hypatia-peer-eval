import eventlet
import socketio
import json
from app.reader import Reader

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
hintCounter = 1

reader = Reader()


# return all elements containing key <key> set to value <value>
# based on https://stackoverflow.com/questions/9807634/
# find-all-occurrences-of-a-key-in-nested-dictionaries-and-lists
def gen_dict_extract(var, key, value):
    if isinstance(var, list):
        for d in var:
            for result in gen_dict_extract(d, key, value):
                yield result
    elif isinstance(var, dict):
        for k, v in var.items():
            if k == key and v == value:
                yield var
            if isinstance(v, dict) or isinstance(v, list):
                for result in gen_dict_extract(v, key, value):
                    yield result
    else:
        print('UNEXPECTED:', var)


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)
    print('check all math:')
    sio.emit('check_all_math')


@sio.on('expressions')
def message_expressions(sid, data):
    print('expressions:\n', data)
    # with open('expression_example.json', 'w') as f:
    #     json.dump(data, f)
    # parser json to python data structure
    record = json.loads(data)
    reader.assignment_from_json_stream(record)
    print('Number of Assignments', len(reader.assignments))
    print('Number of Answers', len(reader.assignments[0].answers))

    # # demo:
    # #   show a yellow box around each plus expression
    # #   Note: make sure to reduce opacity of the color (37 below) otherwise it
    # #   will cover the math
    # for node in list(gen_dict_extract(record, 'command', 'Plus')):
    #   sio.emit('add_box', json.dumps({
    #     "mathid": record["mathid"],
    #     "version": record["version"],
    #     "id": node["id"],
    #     "type": "math-custom",
    #     "hint": "This is an addition recognized by Python",
    #     "color": "#FFFF0037",
    #     "border_color": "#FFFFFFAA",
    #     "border_width": "3px"
    #   }), room=sid)


error_counter = 0


@sio.on('result')
def message_result(sid, data):
    global error_counter
    global hintCounter
    error_counter += 1
    print('result:\n', data)
    # with open('result_example_{}.json'.format(error_counter), 'w') as f:
    #     json.dump(data, f)

    # parser json to python data structure
    record = json.loads(data)
    hint = record['value']['hint'] if 'hint' in record['value'] else None
    if 'id' in record['value']:
        reader.add_error(record['docid'], record['problem'], record['value']['id'], record['value']['type'], hint)
        print("Error added to", record['docid'], record['problem'], record['value']['id'], record['value']['type'],
              hint)
    print(reader.assignments[0].to_json(2))

    assignment = reader.find_assign_with_id(record['docid'])
    answer = assignment.find_answer_with_mathid(record['mathid'])
    generated_highlight_id = answer.generate_highlight_intercept()
    print("trick error at" + generated_highlight_id)
    # add input boxes to real error
    sio.emit('add_input', json.dumps({
        "mathid": record["mathid"],
        "version": record["version"],
        "id": record["value"]["id"],
        "input-id": record["value"]["id"],
        "type": record["value"]["type"],
        "hint": "Type feedback here...",
        "mode": "set"
    }), room=sid)

    # add input box to generated error
    sio.emit('add_input', json.dumps({
        "mathid": record["mathid"],
        "version": record["version"],
        "id": generated_highlight_id,
        "input-id": generated_highlight_id,
        "color": "#ff5040",
        "type": record["value"]["type"],
        "hint": "Type feedback here...",
        "mode": "set"
    }), room=sid)

    # remove all hint
    sio.emit('set_hint', json.dumps({
        "mathid": record["mathid"],
        "version": record["version"],
        "id": record["value"]["id"],
        "type": record["value"]["type"],
        # "hint": "&Hint " + str(hintCounter) + " supplied by <b>Python</b>",
        "mode": "set",
        "enable": False
    }), room=sid)
    # if "hint" not in record["value"]:
    #   sio.emit('set_hint', json.dumps({
    #     "mathid": record["mathid"],
    #     "version": record["version"],
    #     "id": record["value"]["id"],
    #     "type": record["value"]["type"],
    #     "hint": "&Hint " + str(hintCounter) + " supplied by <b>Python</b>",
    #     "mode": "set"
    #   }), room=sid)
    # hintCounter += 1


@sio.on('input_submit')
def print_result(sid, data):
    print('Student Response:\n', data)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 3333)), app)
    # [{'docid': '868.2.12', 'docname': 'Assignment.ezt *', 'userid': 1292, 'username': 'sherry yuan', 'mathid': 'tex8.mth1292-7', 'version': 146, 'problem': 2, 'value': [[{'command': 'Plus', 'id': 'chr1292-13864$chr1292-13866', 'children': [{'command': 'Symbol', 'value': 'a', 'id': 'chr1292-13864$chr1292-13864'}, {'command': 'Symbol', 'value': 'b', 'id': 'chr1292-13866$chr1292-13866'}]}, {'command': '=', 'id': 'chr1292-13869$chr1292-13869'}, {'command': 'Plus', 'id': 'chr1292-13871$chr1292-13963', 'children': [{'command': 'Plus', 'id': 'chr1292-13871$chr1292-13961', 'children': [{'command': 'Number', 'value': '3', 'id': 'chr1292-13871$chr1292-13871'}, {'command': 'Number', 'value': '4', 'id': 'chr1292-13961$chr1292-13961'}]}, {'command': 'Number', 'value': '7', 'id': 'chr1292-13963$chr1292-13963'}]}], [{'command': 'Plus', 'id': 'chr1292-13877$chr1292-13879', 'children': [{'command': 'Number', 'value': '3', 'id': 'chr1292-13877$chr1292-13877'}, {'command': 'Number', 'value': '4', 'id': 'chr1292-13879$chr1292-13879'}]}, {'command': '=', 'id': 'chr1292-13882$chr1292-13882'}, {'command': 'Number', 'value': '7', 'id': 'chr1292-13884$chr1292-13884'}, {'command': '=', 'id': 'chr1292-13966$chr1292-13966'}, {'command': 'Plus', 'id': 'chr1292-13969$chr1292-13971', 'children': [{'command': 'Number', 'value': '8', 'id': 'chr1292-13969$chr1292-13969'}, {'command': 'Number', 'value': '4', 'id': 'chr1292-13971$chr1292-13971'}]}], [{'command': 'Number', 'value': '5', 'id': 'chr1292-13890$chr1292-13890'}, {'command': '=', 'id': 'chr1292-13893$chr1292-13893'}, {'command': 'Number', 'value': '8', 'id': 'chr1292-13895$chr1292-13895'}], [{'command': 'Multiply', 'id': 'chr1292-13901$chr1292-13903', 'children': [{'command': 'Number', 'value': '3', 'id': 'chr1292-13901$chr1292-13901'}, {'command': 'Number', 'value': '5', 'id': 'chr1292-13903$chr1292-13903'}]}, {'command': '=', 'id': 'chr1292-13906$chr1292-13906'}, {'command': 'Number', 'value': '15', 'id': 'chr1292-13908$chr1292-13909'}], [{'command': 'Symbol', 'value': 'l', 'id': 'chr1292-13915$chr1292-13915'}, {'command': '=', 'id': 'chr1292-13918$chr1292-13918'}, {'command': 'Plus', 'id': 'chr1292-13920$chr1292-13923', 'children': [{'command': 'Multiply', 'id': 'chr1292-13920$chr1292-13921', 'children': [{'command': 'Number', 'value': '3', 'id': 'chr1292-13920$chr1292-13920'}, {'command': 'Symbol', 'value': 'x', 'id': 'chr1292-13921$chr1292-13921'}]}, {'command': 'Number', 'value': '5', 'id': 'chr1292-13923$chr1292-13923'}]}], [{'command': 'Derivative', 'id': 'chr1292-13929$chr1292-13935', 'children': [{'command': 'Symbol', 'value': 'l', 'id': 'chr1292-13935$chr1292-13935'}, {'command': 'ExpressionList', 'id': 'chr1292-13938$chr1292-13938', 'children': [{'command': 'Symbol', 'value': 'x', 'id': 'chr1292-13938$chr1292-13938'}]}, {'command': 'Number', 'value': '1'}]}, {'command': '=', 'id': 'chr1292-13942$chr1292-13942'}, {'command': 'Number', 'value': '3', 'id': 'chr1292-13944$chr1292-13944'}]]}]
    #
