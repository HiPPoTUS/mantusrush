from datetime import datetime
import pandas as pd
import data_parser.main as parser


class Simulation(object):
    def __init__(self):
        self.time = datetime.fromtimestamp(0)
        self.lon, self.lat, self.__ice_state = parser.integr_velocity()
        self.ice_state = self.sync()

    def set_time(self, timestamp: float) -> None:
        self.time = datetime.fromtimestamp(timestamp)
        self.ice_state = self.sync()

    def sync(self) -> pd.DataFrame:
        return self.__ice_state[self.time.day]


simulation = Simulation()
