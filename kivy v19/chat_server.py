from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite cereri din alte surse

messages = []

@app.route("/get_messages", methods=["GET"])
def get_messages():
    return jsonify(messages)

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    messages.append({"user": data["user"], "text": data["text"]})
    return jsonify({"status": "received"})

if __name__ == "__main__":
    app.run(port=5000)
