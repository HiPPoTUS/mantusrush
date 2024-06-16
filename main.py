import os

from app.api.server import start
from app.db.main import main as db_start
from app.simulator.main import simulation


def main():
    simulation.sync()

    DB_URL = os.environ.get("DB_URL", "postgresql://postgres:159951@db:5433/ship_schema")
    print(DB_URL)
    db_start()
    start()


if __name__ == '__main__':
    main()
