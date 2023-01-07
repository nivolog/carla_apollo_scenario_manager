class SimAPI(object):
    def __init__(self, **kwargs):
        pass

    def spawn_traffic(self, traffic_data, **kwargs):
        raise NotImplementedError

    def spawn_ego(self, ego_data, **kwargs):
        raise NotImplementedError

    def spawn_vehicle(self):
        raise NotImplementedError
    
    def move_vehicle(self):
        raise NotImplementedError
        