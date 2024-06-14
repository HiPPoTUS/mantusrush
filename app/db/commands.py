import numpy as np

from app.db.migrations import engine, Base, CurrentRoute, PredictedRoute, Route
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


def get_curr_route(idx: int) -> np.ndarray:
    points = session\
        .query(CurrentRoute)\
        .order_by(CurrentRoute.waypoint_time)\
        .filter(CurrentRoute.ship_id == idx)
    route = list()
    for point in points:
        route.append((point.waypoint, point.waypoint_time))

    return np.array(route)
