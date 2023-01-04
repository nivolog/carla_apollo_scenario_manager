
class SimAPI(object):
    def __init__(self, **kwargs):
        pass

    def spawn_traffic(self, **kwargs):
        raise NotImplementedError

    def spawn_vehicle(self, **kwargs):
        raise NotImplementedError
    
    def move_vehicle(self, **kwargs):
        raise NotImplementedError