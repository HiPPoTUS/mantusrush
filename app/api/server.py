from datetime import datetime
import json
import logging

from flask import Flask, Response, request
from http import HTTPStatus
from app.simulator.main import Simulation


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
log = app.logger

simulation = Simulation()


@app.route('/ping')
def ping():
    return 'pong'


@app.route('/update')
def update():
    """
    При вызове метода сервер пойдёт обновлять состояние в сервис за временной меткой, льдом, новыми кораблями,
    после чего начнет считать путь в новой обстановке

    :return: res
    """

    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")
    res.response = json.dumps({
        'message': f'the image has been downloaded.'
    })
    res.content_length = res.calculate_content_length()
    return res


@app.post('/new_ship')
def post_new_ship():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    name = request.form['name']
    file = request.files['img']
    if not file:
        res.status = HTTPStatus.BAD_REQUEST
        res.response = json.dumps({
            'message': "No file loaded"
        })
        res.content_length = res.calculate_content_length()
        log.error('No file loaded')
        return res

    res.response = json.dumps({
        'message': f'the image has been loaded.'
    })
    res.content_length = res.calculate_content_length()
    log.info('%s logged in successfully', name)
    return res


@app.put('/timestamp')
def put_timestamp():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    time = float(request.form['time'])
    simulation.time = datetime.fromtimestamp(time)

    res.response = json.dumps({
        'message': f'time set'
    })
    res.content_length = res.calculate_content_length()
    return res


def start():
    app.run(debug=True)