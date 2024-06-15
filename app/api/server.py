import json
import logging

from flask import Flask, Response, request
from http import HTTPStatus
from app.simulator.main import simulation
import app.db.commands as dbc


app = Flask(__name__)
app.logger.setLevel(logging.INFO)
log = app.logger


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
        'message': f'state successfully updated'
    })
    res.content_length = res.calculate_content_length()
    return res


@app.post('/new_ship')
def post_new_ship():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    name = request.form['name']
    max_speed = request.form['max_speed']
    ice_class = request.form['ice_class']

    result = dbc.new_ship(name, float(max_speed), int(ice_class))

    if not result:
        res.status = HTTPStatus.BAD_REQUEST
        res.response = json.dumps({
            'message': "bad request"
        })
        res.content_length = res.calculate_content_length()
        log.error('New ship bad request')
        return res

    res.response = json.dumps({
        'message': f'new ship created.'
    })
    res.content_length = res.calculate_content_length()
    log.info('logged in successfully')

    return res


@app.get('/way/<way_type>/<int:ship_id>')
def get_route(way_type, ship_id):
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    ship = dbc.get_ship(ship_id)
    print(ship.ship_id)
    route = dbc.get_route(-1, ship.ship_id)
    print(route)
    if way_type == "current":
        way = dbc.get_current_route(route.route_id)
        way = {"current": way.tolist()}
    elif way_type == "prediction":
        way = dbc.get_predicted_route(route.route_id)
        way = {"prediction": way.tolist()}
    else:
        way1 = dbc.get_current_route(route.route_id)
        way2 = dbc.get_predicted_route(route.route_id)
        way = {"current": way1.tolist(), "prediction": way2.tolist()}

    res.response = json.dumps(way)
    res.content_length = res.calculate_content_length()
    return res


@app.post('/new_route')
def post_new_route():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    ship_idx = int(request.form['ship_idx'])
    start_point_idx = int(request.form['start_point_idx'])
    end_point_idx = int(request.form['end_point_idx'])
    start_time = float(request.form['end_point_idx'])

    result = dbc.new_route(ship_idx, start_point_idx, end_point_idx, start_time)

    if not result:
        res.status = HTTPStatus.BAD_REQUEST
        res.response = json.dumps({
            'message': "bad request"
        })
        res.content_length = res.calculate_content_length()
        log.error('New route bad request')
        return res

    res.response = json.dumps({
        'message': f'new route created.'
    })
    res.content_length = res.calculate_content_length()
    log.info('logged in successfully')
    return res


@app.put('/timestamp/<float:time>')
def put_timestamp(time):
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    simulation.set_time(time)
    print(simulation.time)
    res.response = json.dumps({
        'message': f'time set'
    })
    res.content_length = res.calculate_content_length()
    return res


def start():
    app.run(debug=True)
