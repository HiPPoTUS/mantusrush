from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import CreateSchema

# Параметры подключения к базе данных
DB_URL = "postgresql://postgres:159951@:5432/ship_schema"

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


class Ship(Base):
    __tablename__ = 'ships'
    __table_args__ = {'schema': 'ship_schema'}
    ship_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    type = Column(String(50))
    description = Column(String)
    max_speed = Column(DECIMAL(5, 2), nullable=False)
    ice_class = Column(Integer, nullable=False)


class Route(Base):
    __tablename__ = 'routes'
    __table_args__ = {'schema': 'ship_schema'}
    route_id = Column(Integer, primary_key=True, autoincrement=True)
    ship_id = Column(Integer, ForeignKey('ship_schema.ships.ship_id'), nullable=False)
    start_point = Column(Integer, ForeignKey('ship_schema.ports.port_id'), nullable=False)
    end_point = Column(Integer, ForeignKey('ship_schema.ports.port_id'), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    arrival_time = Column(TIMESTAMP, nullable=True)


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
