from app.api.server import start
from app.db.main import main as db_start
from app.simulator.main import simulation


def main():
    simulation.sync()
    db_start()
    start()


if __name__ == '__main__':
    main()
