import time

# TODO: Import apollo messages

# TODO: from apollo_api import ApolloAPI
from carla_api import CarlaAPI
from data_reader import DataReader
from recorder.data_recorder import DataRecorder

class Scenario():
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.host = kwargs['host']
        self.port = kwargs['port']
        self.fps = kwargs['fps']
        self.timeout = kwargs['timeout']
        self.scenario = kwargs['scenario']
        self.path = kwargs['path']
        self.prefix = kwargs['prefix']
        
        self.init_actors_position = []
        self.init_ego_position = [0,0,0,0]

        self.actors = []
        self.traffic = []
        self.ego = None

        self.API = None
        self.data_reader = DataReader()
        self.recorder = DataRecorder()

        self.start = False

    def load_scenario(self): #DONE
        if self.path is not None:
            path = self.path
        else:
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
            return True
        else:
            print('Error on loading scenario')
            return False

    def prepare_scenario(self): # TODO: check Carla implementation, add Apollo
        if self.kwargs['simuator'].lower() == 'carla':
            self.API = CarlaAPI(**self.kwargs)
        elif self.kwargs['simuator'].lower() == 'apollo':
            # self.API = ApolloAPI(**self.kwargs)
            pass
        else:
            print('Unsupported simulator "{}" provided'.format(self.kwargs['simulator']))
        
        #spawn traffic vehicles
        self.traffic = self.API.spawn_traffic(**self.kwargs)
        #spawn ego
        self.ego = self.API.spawn_ego(**self.kwargs)

        #check what we have spawned
        self.actors = [self.ego] + self.traffic
        if not all(self.actors):
            print(self.actors)
            print('Some actors are None')
            return False
        return True

    
    def launch_scenario(self): # TODO: Start moving vehicles, pass to planner routing request
        #Get everything moving, maybe start recording data
        pass

    def manage_traffic(self): # TODO: manage either traffic autopilot or traffic movement control
        #Set autopilot, or manage each traffic individually
        pass
    
    def check_stop_condition(self): # TODO: add checking vehicle position
        # Here we check if scenario should end
        return False

    def sim_loop(self): #TODO: check if something is needed
        # This part prevents traffic to drive at the begiinning, waiting for player to start them manually
        try:
            if not self.start:
                start_sim = raw_input('Start simulation? ([y]/n): ')
                if start_sim.strip() == 'y':
                    self.launch_scenario()
                    return True
                else:
                    return False
            
            self.recorder.record_one_time()
            
            if (self.check_stop_condition()):
                return False
            # Shhh... it's dreaming!
            time.sleep(1/self.fps)
            return True
        except KeyboardInterrupt:
            print('interrupt')
            return False

