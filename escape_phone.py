from flask import Flask, request
from multiprocessing import Process, Pipe
import phone_control
import json

app = Flask(__name__, static_url_path='')
flask_conn, phone_conn = Pipe()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/json_test')
def jsonTest():
    return app.send_static_file('json_test.html')


if __name__ == '__main__':

    phoneControl = Process(target=phone_control.main, args=(phone_conn,))
    phoneControl.start()

    app.run(debug=False, threaded=True)
