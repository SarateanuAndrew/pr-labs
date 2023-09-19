from flask import Flask, request

app = Flask(__name__)


@app.route('/hello', methods=["GET", "POST"])
def hello_world():  # put application's code here
    if request.method == "GET":
        return {"Message" : "hello"}
    elif request.method == "POST":
        payload = request.json
        for key, value in payload.items():
            print(f"{key} : {value}")
            return "confirmation"


if __name__ == '__main__':
    app.run()
