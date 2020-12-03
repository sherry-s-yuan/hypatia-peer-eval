import eventlet
import socketio
import json
import requests
from app.reader import Reader

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)
hintCounter = 1

reader = Reader()
db_data = {}


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
    reader.record_error_count()
    reader.record_total_highlight()
    print('result:\n', data)

    # parser json to python data structure
    record = json.loads(data)
    hint = record['value']['hint'] if 'hint' in record['value'] else None
    if 'id' in record['value']:
        reader.add_error(record['docid'], record['problem'],
                         record['value']['id'], record['value']['type'], hint)
        print("Error added to", record['docid'], record['problem'],
              record['value']['id'], record['value']['type'],
              hint)
    format_data_to_db(record, record['problem'])

    assignment = reader.find_assign_with_id(record['docid'])
    answer = assignment.find_answer_with_mathid(record['mathid'])
    generated_highlight_id = answer.generate_highlight_intercept()
    print("generated id", generated_highlight_id)

    # add input boxes to real error
    print("input-id", record["value"]["id"])
    sio.emit('add_input', json.dumps({
        "mathid": record["mathid"],
        "version": record["version"],
        "id": record["value"]["id"],
        "input-id": record["value"]["id"],
        "type": record["value"]["type"],
        "hint": "Type feedback here...",
        "mode": "set"
    }), room=sid)
    if generated_highlight_id is not None:
        reader.record_total_highlight()
        # add input box to generated error
        sio.emit('add_input', json.dumps({
            "mathid": record["mathid"],
            "version": record["version"],
            "id": generated_highlight_id,
            "input-id": generated_highlight_id,
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
        "mode": "set",
        "enable": False
    }), room=sid)


@sio.on('input_submit')
def print_result(sid, data):
    record = json.loads(data)
    db_data["editor_id"] = record["userid"]
    if "id" in record["value"]:
        docid, id, feedback = record["docid"], record["value"]["id"], \
                              record["value"]["response"]
        if id is None:
            print("Something Went Wrong, Please Try Again")
            return
        id = id.rstrip('-button')
        correct = reader.record_feedback_score(docid, id, feedback)

    print("Your current score is: ", reader.calculate_score())
    reader.print_scores()

    # Once the editor has inputted all the feedback, the information gets sent to the databse
    if reader.num_error == reader.trial:
        db_data["score"] = reader.calculate_score()*100
        print(db_data)
        db_data["feedback"] = reader.id2feedback
        url = "http://127.0.0.1:8000/home/save"
        result = requests.post(url, json.dumps(db_data))
        if str(result.status_code) != "200":
            print("Failed")
            print(result.text)
        else:
            print("Success!")


def format_data_to_db(record, problem_num):
    print(problem_num)
    if len(db_data) == 0:
        db_data["userid"] = record["userid"]
        db_data["docid"] = ".".join([record["docid"].rsplit(".", 1)[0],
                                     str(db_data["userid"])])
        db_data["answers"] = {}
        db_data["contains_error"] = False
        for answer in reader.assignments[0].answers:
            for line in answer.lines:
                if line.contains_error:
                    db_data["contains_error"] = True
                    break

    if problem_num not in db_data["answers"]:
        db_data["answers"][problem_num] = []
    for i in range(len(reader.assignments[0].to_json(problem_num))):
        if reader.assignments[0].to_json(problem_num)[i]["value"] \
                not in db_data["answers"][problem_num]:
            db_data["answers"][problem_num].append(
                reader.assignments[0].to_json(problem_num)[i][
                    "value"])
            print(db_data)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 3333)), app)

