from flask import abort, Flask, jsonify, request
from flair.data import Sentence
from flair.models import SequenceTagger


app = Flask(__name__)


# load the model
model = SequenceTagger.load_from_file('best-model.pt')


@app.route('/api/v1/ping')
def ping():
    response = {"ping": "pong"}
    return jsonify(response), 200


@app.route('/api/v1/parseReceipt', methods=['POST'])
def parseReceipt():
    response_list = list()

    if not request.json or not 'receipt' in request.json:
        abort(400)
    receipt = request.json['receipt']

    # create a sentences
    lines = receipt.split('\n')
    for index, line in enumerate(lines):
        if line.strip():
            sentence = Sentence(line)

            # predict tags and print
            model.predict(sentence)

            # add prediction to response
            response_list.append({f"LINE_{index}": sentence.to_dict(tag_type='ner')})

    print(response_list)
    response = response_list
    return jsonify(response), 200


if __name__ == "__main__":
    app.run()
