import glob
import os
import sys

from sim_api import SimAPI

try:
    sys.path.append(glob.glob('../carla-python-0.9.13/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    print('Cannot import CARLA module')
    pass
import carla

class CarlaAPI(SimAPI):
    client = None
    world = None
    
    def __init__(self, **kwargs):
        super(SimAPI, self).__init__(kwargs)
        self.client = carla.Client(kwargs['host'], kwargs['port'])
        if kwargs['timeout']:
            self.client.set_timeout(kwargs['timeout'])
        self.world = self.client.get_world()

    def spawn_traffic(self, **kwargs): # TODO: add vehicl spawning with returning vehicle list, paramterize bp filtering
        bp_lib = self.world.get_blueprint_library().filter('vehicle.dodge.charger_police')
        raise NotImplementedError

    def spawn_vehicle(self, **kwargs): # TODO: add bp filtering, add vehicle spawning
        raise NotImplementedError
    
    def move_vehicle(self, **kwargs): # TODO: add vehicle moving via its id or instance
        raise NotImplementedError
