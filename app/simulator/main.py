from datetime import datetime


class Simulation(object):
    def __init__(self):
        self.time = datetime.fromtimestamp(0)
        self.IceState = None

