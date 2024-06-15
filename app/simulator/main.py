from datetime import datetime
import pandas as pd
import data_parser.main as parser


class Simulation(object):
    def __init__(self):
        self.lon, self.lat, self.__ice_state, self.__dates = parser.integr_velocity()
        self.time = self.__dates[0]
        print(self.__dates)
        self.ice_state = self.sync()

    def set_time(self, timestamp: float) -> None:
        self.time = timestamp
        self.ice_state = self.sync()

    def sync(self) -> pd.DataFrame:
        for i in range(len(self.__dates) - 1):
            if self.__dates[i] <= self.time < self.__dates[i + 1]:
                return self.__ice_state[i]
        return self.__ice_state[-1]


simulation = Simulation()
