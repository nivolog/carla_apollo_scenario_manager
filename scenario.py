import time
from math import hypot
# TODO: Import apollo messages

# TODO: from apollo_api import ApolloAPI
from carla_api import CarlaAPI
from data_reader import DataReader
from recorder.data_recorder import DataRecorder

class Scenario():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        # Usual simulation server options
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.fps = kwargs.get('fps')
        self.timeout = kwargs.get('timeout')
        
        # Scenario options
        self.scenario = kwargs.get('scenario')
        self.path = kwargs.get('path')
        self.prefix = kwargs.get('prefix')
        
        self.init_actors_position = []
        self.init_ego_position = [0,0,0,0]

        self.actors = []
        self.traffic = []
        self.ego = None
        self.traffic_autopilot = False
        
        # Scenario components
        self.API = None
        self.data_reader = DataReader()
        self.recorder = DataRecorder()

        self.autostart = kwargs.get('autostart')
        self.start = False

        self.stop_state = None
        self.stop = True
        
    def load_scenario(self):
        if self.path is not None:
            # Path to scenario file
            path = self.path
        else:
            # TODO: remove hardcode
            if self.scenario == 'circle':
                path = 'data/circle_town03.xml'
            elif self.scenario == 'straight':
                path = 'data/straight_town03.xml'
            elif self.scenario == 'uncontrolled_intersection':
                path = 'data/uncontrolled_intersection_skolkovo_big.xml'
            else:
                path = None
                print('Wrong scenario provided')
                return False
        if self.data_reader.read_data(path):
            self.init_actors_position = self.data_reader.get_actors()
            self.init_ego_position = self.data_reader.get_ego()
            self.stop_state = self.data_reader.get_stop()
            return True
        else:
            print('Error on loading scenario')
            return False

    def prepare_scenario(self): # TODO: check Carla implementation, add Apollo
        # Get required API to manage traffic and ego
        if self.kwargs['simuator'].lower() == 'carla':
            self.API = CarlaAPI(**self.kwargs)
        elif self.kwargs['simuator'].lower() == 'apollo':
            # self.API = ApolloAPI(**self.kwargs)
            pass
        else:
            print('Unsupported simulator "{}" provided'.format(self.kwargs['simulator']))
        
        # Spawn traffic vehicles
        self.traffic = self.API.spawn_traffic(self.init_actors_position, **self.kwargs)
        # Spawn ego
        self.ego = self.API.spawn_ego(self.init_ego_position, **self.kwargs)

        # Check what we have spawned
        self.actors = [self.ego] + self.traffic
        if not all(self.actors):
            print(self.actors)
            print('Some actors are None')
            return False
        return True

    
    def launch_scenario(self): # TODO: Start moving vehicles, pass to planner routing request
        # TODO: Send routing request to apollo system
        # self.apollo_features.send_routing_request()
        
        # If autopilot is in options and current simulator is Carla
        # then autopilot is applied to each car in simulation
        if self.kwargs['simuator'].lower() == 'carla':
            if self.kwargs['traffic_autopilot'].lower() == 'true':
                self.traffic_autopilot = True
                self.API.set_autopilot(self.traffic)
        
        # TODO: Start recording all the metrics
        # NOTE: recorder requires full refactoring 
        # self.recorder.start_recording()
        pass
    
    def manage_traffic(self): # TODO: manage traffic movement control
        # TODO: Manage each traffic car individually
        pass
    
    def check_stop_condition(self): # TODO: add checking vehicle position
        # Here we check if scenario should end
        # TODO: Add other checks, e.g. timeout or ego stuck
        #Basic check on scenario end
        t = self.ego.get_transform()
        dist = hypot(self.stop_condition[0] - t.location.x, self.stop_condition[1] - t.location.y)
        if dist < 1: #TODO: parametrize this
            return True
        return False
    
    def sim_loop(self): #TODO: check if something is needed
        #If autostart is in options, scenario will start immidiatly
        if self.autostart is not None and self.autostart == 'True':
            self.start = True
            
        try:
            # This part prevents traffic to drive at the begiinning, waiting for player to start them manually
            if not self.start:
                start_sim = raw_input('Start simulation? ([y]/n): ')
                if start_sim.strip() in ['y','yes','д', 'да']:
                    self.launch_scenario()
                    self.start = True
                    self.stop = False
                    return True
                else:
                    return False
            
            #self.recorder.record_one_time()
            
            # If autopilot is not set, manage each car individual path
            if not self.traffic_autopilot:
                self.manage_traffic()

            # Check any reasons why scenario should end
            if self.check_stop_condition():
                self.stop = True
                return False
            # Shhh... it's dreaming!
            time.sleep(1/self.fps)
            return True
        except KeyboardInterrupt:
            print('Cancelled by user. Bye!')
            self.stop = True
            return False

