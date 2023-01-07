import glob
from numpy.random import choice
import os
import sys

from sim_api import SimAPI

try:
    sys.path.append(glob.glob('./carla/dist/carla-*%d.%d-%s.egg' % (
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
        self.bp_lib = self.world.get_blueprint_library()

    def spawn_traffic(self, traffic_data,  **kwargs): # TODO: check
        if traffic_data is None:
            print('No traffic data provided. Cannot spawn actors')
            return []

        traffic_bp = self.bp_lib.filter(kwargs['traffic_filter']) #'vehicle.dodge.charger_police'
        self.traffic_data = traffic_data
        traffic_list = []
        for car in self.traffic_data:
            pos = car[1]
            spawn_point = carla.Transform(carla.Location(x=pos[0],y=pos[1], z=pos[2]), carla.Rotation(yaw=pos[3]))
            bp = choice(traffic_bp)
            bp.set_attribute('role_name', 'traffic')
            actor = self.spawn_vehicle(vehicle_data = [spawn_point, bp])            
            if actor is None:
                print('Cannot spawn vehicle at {}'.format(spawn_point))
            else:
                print('Spawned actor {} at {}'.format(actor, spawn_point))
                actor.set_autopilot(False)
                traffic_list.append(actor)
        return traffic_list

    def spawn_ego(self, ego_data, **kwargs): # TODO: add vehicle spawning
        if ego_data is None:
            print('No ego data provided. Cannot spawn ego')
            return None

        ego_bp = self.bp_lib.filter(kwargs['ego_filter'])
        bp = choice(ego_bp)
        spawn_point = carla.Transform(carla.Location(x=ego_data[0],y=ego_data[1], z=ego_data[2]), carla.Rotation(yaw=ego_data[3]))
        actor = self.spawn_vehicle(vehicle_data = [spawn_point, bp])
        if actor is None:
                print('Cannot spawn vehicle at {}'.format(spawn_point))
        else:
            print('Spawned actor {} at {}'.format(actor, spawn_point))
            actor.set_autopilot(False)
        return actor

    def spawn_vehicle(self, vehicle_data): # TODO: add vehicle spawning
        actor = None
        tries = 0
        while actor is None and tries <= 10:
            actor = self.world.try_spawn_actor(vehicle_data[1], vehicle_data[0])
            tries += 1                
            if actor is None:
                print('Cannot spawn actor at {}. Try #{}'.format(vehicle_data[0], tries))
        return actor
    
    def move_vehicle(self, **kwargs): # TODO: add vehicle moving via its id or instance
        raise NotImplementedError
