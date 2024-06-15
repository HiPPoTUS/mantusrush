import numpy as np
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.db.migrations import engine, Base, CurrentRoute, PredictedRoute, Route, Ship
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def get_ship(idx: int) -> Ship:
    ship = session \
        .query(Ship) \
        .filter(Ship.ship_id == idx) \
        .first()

    return ship


def new_ship(name: str, max_speed: float, ice_class: int) -> bool:
    ship = Ship(name=name, max_speed=max_speed, ice_class=ice_class)
    session.add(ship)
    try:
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        return False
    finally:
        session.close()


def get_route(route_idx: int, ship_idx: int) -> Route | None:
    route = None
    if ship_idx == -1:
        route = session \
            .query(Route) \
            .filter(Route.route_id == route_idx) \
            .first()
    elif route_idx == -1:
        route = session \
            .query(Route) \
            .filter(Route.ship_id == ship_idx) \
            .first()
    return route


def new_route(ship_idx: int, start_point_idx: int, end_point_idx: int, start_time: float) -> bool:
    route = Route(ship_id=ship_idx, start_point=start_point_idx, end_point=end_point_idx, start_time=datetime.fromtimestamp(start_time))
    session.add(route)
    try:
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        return False
    finally:
        session.close()


def get_predicted_route(idx: int) -> np.ndarray:
    points = session \
        .query(PredictedRoute) \
        .order_by(PredictedRoute.waypoint_time) \
        .filter(PredictedRoute.route_id == idx)
    route = list()
    for point in points:
        route.append((point.waypoint, point.waypoint_time))

    return np.array(route)


def get_current_route(idx: int) -> np.ndarray:
    points = session\
        .query(CurrentRoute)\
        .order_by(CurrentRoute.waypoint_time)\
        .filter(CurrentRoute.route_id == idx)
    route = list()
    for point in points:
        route.append((point.waypoint, point.waypoint_time))

    return np.array(route)
