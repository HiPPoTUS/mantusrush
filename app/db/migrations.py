from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import CreateSchema
from sqlalchemy.sql import func

from typing import Optional, List, Any, TypeVar, Callable


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


# Параметры подключения к базе данных
DB_URL = "postgresql://postgres:159951@0.0.0.0:5432/ship_schema"

# Создание подключения к базе данных
engine = create_engine(DB_URL)
Base = declarative_base()


# Определение моделей
class Port(Base):
    __tablename__ = 'ports'
    __table_args__ = {'schema': 'ship_schema'}
    port_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    coordinates = Column(String(100), nullable=False)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.port_id is not None:
            result["port_id"] = from_union([from_int, from_none], self.port_id)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.coordinates is not None:
            result["coordinates"] = from_union([from_str, from_none], self.coordinates)
        return result


class Ship(Base):
    __tablename__ = 'ships'
    __table_args__ = {'schema': 'ship_schema'}
    ship_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(String(50))
    description = Column(String)
    max_speed = Column(DECIMAL(5, 2), nullable=False)
    ice_class = Column(Integer, nullable=False)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.ship_id is not None:
            result["ship_id"] = from_union([from_int, from_none], self.ship_id)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        if self.type is not None:
            result["type"] = from_union([from_str, from_none], self.type)
        if self.description is not None:
            result["description"] = from_union([from_str, from_none], self.description)
        if self.max_speed is not None:
            result["max_speed"] = float(self.max_speed)
        if self.ice_class is not None:
            result["ice_class"] = from_union([from_int, from_none], self.ice_class)
        return result


class Route(Base):
    __tablename__ = 'routes'
    __table_args__ = {'schema': 'ship_schema'}
    route_id = Column(Integer, primary_key=True, autoincrement=True)
    ship_id = Column(Integer, ForeignKey('ship_schema.ships.ship_id'), nullable=False)
    start_point = Column(Integer, ForeignKey('ship_schema.ports.port_id'), nullable=False)
    end_point = Column(Integer, ForeignKey('ship_schema.ports.port_id'), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    arrival_time = Column(TIMESTAMP, nullable=True)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.route_id is not None:
            result["route_id"] = from_union([from_int, from_none], self.route_id)
        if self.ship_id is not None:
            result["ship_id"] = from_union([from_int, from_none], self.ship_id)
        if self.start_point is not None:
            result["start_point"] = from_union([from_int, from_none], self.start_point)
        if self.end_point is not None:
            result["end_point"] = from_union([from_int, from_none], self.end_point)
        if self.start_time is not None:
            result["start_time"] = self.start_time.timestamp()
        if self.arrival_time is not None:
            result["arrival_time"] = self.arrival_time.timestamp()
        return result


class SimlifyRoute(object):
    def __init__(self, route_id, ship_id, route, start_time):
        self.route_id = route_id
        self.ship_id = ship_id
        self.route = route
        self.start_time = start_time

    route_id: int
    ship_id: int
    route: [[float, float], [float, float]]
    start_time: datetime

    def to_dict(self) -> dict:
        result: dict = {}
        if self.route_id is not None:
            result["route_id"] = from_union([from_int, from_none], self.route_id)
        if self.ship_id is not None:
            result["ship_id"] = from_union([from_int, from_none], self.ship_id)
        if self.route is not None:
            result["route"] = self.route
        if self.start_time is not None:
            result["start_time"] = self.start_time.timestamp()
        return result


class CurrentRoute(Base):
    __tablename__ = 'current_routes'
    __table_args__ = {'schema': 'ship_schema'}
    current_route_id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('ship_schema.routes.route_id'), nullable=False)
    waypoint = Column(String(100), nullable=False)
    waypoint_time = Column(TIMESTAMP, nullable=False)


class PredictedRoute(Base):
    __tablename__ = 'predicted_routes'
    __table_args__ = {'schema': 'ship_schema'}
    predicted_route_id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('ship_schema.routes.route_id'), nullable=False)
    waypoint = Column(String(100), nullable=False)
    waypoint_time = Column(TIMESTAMP, nullable=False)


def create_schema_if_not_exists():
    with engine.connect() as connection:
        connection.execute(CreateSchema("ship_schema", if_not_exists=True))
        connection.commit()


def create_tables_if_not_exists():
    Base.metadata.create_all(engine)


def main():
    with engine.connect() as connection:
        with connection.begin():
            create_schema_if_not_exists()
            create_tables_if_not_exists()
    print("Схема и таблицы успешно созданы или уже существуют.")


if __name__ == "__main__":
    main()
