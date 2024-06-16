import json
import logging
import time
from datetime import datetime

from flask import Flask, Response, request
from flask_cors import CORS
from http import HTTPStatus

from app.db.migrations import SimlifyRoute, Ship
from app.simulator.main import simulation
import app.db.commands as dbc

format_string = '%Y-%m-%dT%H:%M:%S.%fZ'

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.INFO)
log = app.logger


@app.route('/ping')
def ping():
    return 'pong'


@app.post('/update')
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
    time.sleep(3)
    res.content_length = res.calculate_content_length()
    return res


@app.post('/new_ship')
def post_new_ship():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")
    data = request.get_json()
    print(data)
    name = data.get("name")
    max_speed = float(data.get("max_speed"))
    ice_class = int(data.get("ice_class"))

    ship_id = dbc.new_ship(name, max_speed, ice_class)
    if ship_id == -1:
        res.status = HTTPStatus.BAD_REQUEST
        res.response = json.dumps({
            'message': "bad request"
        })
        res.content_length = res.calculate_content_length()
        log.error('New ship bad request')
        return res

    ship = Ship(ship_id=ship_id, name=name, max_speed=max_speed, ice_class=ice_class)

    res.response = json.dumps(ship.to_dict())
    res.content_length = res.calculate_content_length()
    log.info('logged in successfully')

    return res


@app.get('/way/<way_type>/<int:ship_id>')
def get_route(way_type, ship_id):
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    ship = dbc.get_ship(ship_id)
    route = dbc.get_route(-1, ship.ship_id)
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


@app.get('/routes')
def get_routes():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    routes = dbc.get_routes()
    routes = [route.to_dict() for route in routes]

    res.response = json.dumps(routes)
    res.content_length = res.calculate_content_length()
    return res


@app.get('/routes/simplify')
def get_routes_simple():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    routes = dbc.get_routes()
    simplify_routes = list()
    for route in routes:
        if route.end_point == 48:
            continue
        start = dbc.get_port(route.start_point).coordinates
        end = dbc.get_port(route.end_point).coordinates
        route_s = [start.split(' '), end.split(' ')]
        simplify_routes.append(SimlifyRoute(route.route_id, route.ship_id, route_s, route.start_time))
    simplify_routes = [route.to_dict() for route in simplify_routes]

    res.response = json.dumps(simplify_routes)
    res.content_length = res.calculate_content_length()
    return res


@app.get('/ship/<int:ship_id>')
def get_ship(ship_id):
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    ship = dbc.get_ship(ship_id)

    res.response = json.dumps(ship.to_dict())
    res.content_length = res.calculate_content_length()
    return res


@app.get('/ships')
def get_ships():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    ships = dbc.get_ships()
    ships = [ship.to_dict() for ship in ships]

    res.response = json.dumps(ships)
    res.content_length = res.calculate_content_length()
    return res


@app.get('/ports')
def get_ports():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")

    ports = dbc.get_ports()
    ports_r = list()
    for port in ports:
        if port.port_id == 48:
            continue
        ports_r.append(port.to_dict())
    # ports = [port.to_dict() for port in ports]

    res.response = json.dumps(ports_r)
    res.content_length = res.calculate_content_length()
    return res


@app.post('/new_route')
def post_new_route():
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")
    data = request.get_json()
    print(data)
    ship_idx = data.get("ship_id")
    start_point_idx = data.get("start_point_idx")
    end_point_idx = data.get("end_point_idx")
    start_time = datetime.strptime(data.get("start_time"), format_string)

    route_id = dbc.new_route(ship_idx, start_point_idx, end_point_idx, start_time)

    if route_id == -1:
        res.status = HTTPStatus.BAD_REQUEST
        res.response = json.dumps({
            'message': "bad request"
        })
        res.content_length = res.calculate_content_length()
        log.error('New route bad request')
        return res

    start = dbc.get_port(start_point_idx).coordinates
    end = dbc.get_port(end_point_idx).coordinates
    route_s = [start.split(' '), end.split(' ')]
    simplify_route = SimlifyRoute(route_id, ship_idx, route_s, start_time)

    res.response = json.dumps(simplify_route.to_dict())
    res.content_length = res.calculate_content_length()
    log.info('logged in successfully')
    return res


@app.put('/timestamp/<timestamp>')
def put_timestamp(timestamp):
    res = Response(response="None", status=HTTPStatus.OK, mimetype="application/json")
    timestamp = float(timestamp)
    simulation.set_time(timestamp)
    print(simulation.time)
    res.response = json.dumps({
        'message': f'time set'
    })
    res.content_length = res.calculate_content_length()
    return res


def start():
    app.run(debug=False)
