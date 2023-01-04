from math import hypot 

class BasicManeuver(object):
    start_ego_position = None
    goal_ego_position = None
    ego = None
    stop_condition = None
    traffic_data = [] # Contains (start transform, blueprint, set_of_waypoint or autopilot)
    traffic = []
    data_recorder = None
    
    def __init__(self):
        self.start_ego_position = None
        self.goal_ego_position = None
        self.ego = None
        self.traffic_data = [] # Contains (start transform, blueprint, set_of_waypoint or autopilot)
        self.traffic = []
        self.data_recorder = None

    def spawn_traffic(self, world, traffic_data = None):
        if traffic_data is not None:
            self.traffic_data = traffic_data
        
        if traffic_data is None:
            print('No traffic data provided. Cannot spawn actors')
            return
        
        for car in self.traffic_data:
            car[1].set_attribute('role_name', 'traffic')
            actor = self.spawn_actor(data=car, world=world)
            if actor is not None:
                self.traffic.append(actor)

    def spawn_actor(self, data, world):
        actor = world.try_spawn_actor(data[1], data[0])
        if actor is None:
            print('Cannot spawn actor at {}'.format(data[0]))
            return actor

        if isinstance(data[2], bool):
            # actor.set_autopilot(data[2])
            actor.set_autopilot(False)
        elif isinstance(data[2], list):
            self.apply_custom_traffic_path(actor)
        else:
            print('Unknown driving mode for vehicle {}'.format(actor))
        
        print('Spawned actor {} at {}'.format(actor, data[0]))
        return actor

    def apply_custom_traffic_path(self, actor):
        raise NotImplementedError
    
    def set_traffic_autopilot(self):
        for actor, data in zip(self.traffic, self.traffic_data):
            actor.set_autopilot(data[2])

    def set_stop_condition(self, stop):
        self.stop_condition = stop

    def check_stop_condition(self):
        t = self.ego.get_transform()
        dist = hypot(self.stop_condition[0] - t.location.x, self.stop_condition[1] - t.location.y)
        if dist < 3:
            return True
        return False

    def spawn_ego(self, ego_data, world):
        ego_data[1].set_attribute('role_name', 'hero')
        ego_actor = self.spawn_actor(data=ego_data, world=world)
        if ego_actor is None:
            print('Failed to spawn ego')
        self.ego = ego_actor
        self.start_ego_position = ego_data[0]
        self.goal_ego_position = ego_data[2][-1]
    
    def set_ego(self, ego):
        self.ego = ego

    def teleport_ego(self, transform):
        self.ego.set_transform(transform)


    def send_routing_request(self):
        raise NotImplementedError
        #magic_function_send_routing_request_to_apollo(self.start_ego_position, self.goal_ego_position)

    def __del__(self):
        for actor in self.traffic:
            print('Destroying actor {}'.format(actor))
            actor.destroy()