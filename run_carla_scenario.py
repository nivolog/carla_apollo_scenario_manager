import argparse
import glob
import numpy as np
import os
import sys
import time
import datetime

try:
    sys.path.append(glob.glob('../carla-python-0.9.13/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    print('Cannot import CARLA module')
    pass
import carla



try:
    from data_recorder import DataRecorder
except ImportError:
    try:
        sys.path.append(glob.glob('../carla-statistics/'))
        from data_recorder import DataRecorder
    except IndexError:
        print('Cannot import statistics module')
        pass

from basic_maneuver import BasicManeuver
from data_reader import DataReader

def loop(start, scenario, recorder, fps):
    # This part prevents traffic to drive at the begiinning, waiting for player to start them manually
    try:
        if not start:
            start_sim = raw_input('Start simulation? ([y]/n): ')
            if start_sim.strip() == 'y':
                scenario.set_traffic_autopilot()
                return True
            else:
                return False
        
        recorder.record_one_time()
        
        if (scenario.check_stop_condition()):
            return False
        # Shhh... it's dreaming!
        time.sleep(1/fps)
        return True
    except KeyboardInterrupt:
        print('interrupt')
        return False

class Scenario():
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.fps = args.fps
        self.timeout = args.timeout
        self.scenario = args.scenario
        self.path = args.path
        self.prefix = args.prefix
        
        
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost',
                    help='IP of the host server (default: localhost)')
    parser.add_argument('--port', default=2000, type=int,
                    help='TCP port to listen to (default: 2000)')
    parser.add_argument('--fps', default=30.0, type=float,
                    help='Rate at which recorder will record data')
    parser.add_argument('--timeout', default=300.0, type=float,
                    help='Set the CARLA client timeout value in seconds')
    parser.add_argument('--scenario', default='circle', type=str,
                    help='Defines scenario type you are willing to launch')
    parser.add_argument('--path', default=None, type=str,
                    help='Path to scenario data file. Overrides \'scenario\' argument')
    parser.add_argument('--prefix', default='Manual', type=str,
                    help='Prefix to log output')
    args = parser.parse_args()
    
    # Create data reader instance for parsing xml with traffic and ego position
    data_reader = DataReader()

    # Read data of particular scenario
    if args.path is not None:
        path = args.path
    else:
        if args.scenario == 'circle':
            path = 'data/circle_town03.xml'
        elif args.scenario == 'straight':
            path = 'data/straight_town03.xml'
        elif args.scenario == 'uncontrolled_intersection':
            path = 'data/uncontrolled_intersection_skolkovo_big.xml'
        else:
            path = None
            print('Wrong scenario provided')
            return
    actors = []
    if data_reader.read_data(path):
        actors = data_reader.get_actors()
    else:
        print('Error on loading scenario')
        return
    
    # Create scenario/maneuver instance that will automaticly manage traffic and ego
    scenario = BasicManeuver()

    # Connect Carla
    client = carla.Client(args.host, args.port)
    if args.timeout:
        client.set_timeout(args.timeout)
    world = client.get_world()
    
    # Spawn traffic
    bp_lib = world.get_blueprint_library().filter('vehicle.dodge.charger_police')
    traffic_data = []
    for actor in actors:
        pos = actor[1]
        spawn_point = carla.Transform(carla.Location(x=pos[0],y=pos[1], z=pos[2]), carla.Rotation(yaw=pos[3]))
        bp = np.random.choice(bp_lib)
        traffic_data.append([spawn_point, bp, actor[2]])
    scenario.spawn_traffic(world, traffic_data)

    # Get ego vehicle and teleport it to starting location
    ego = world.get_actors().filter('vehicle.lincoln.mkz*')
    if ego is None:
        print('No ego vehicle found in simulation. Abortion')
        return
    else:
        if len(ego) > 1:
            print('Warning. Found more than one ego-like vehicles. Picking first one')
        ego = ego[0]
    scenario.set_ego(ego)
    ego_pos = data_reader.get_ego()
    ego_pos = carla.Transform(carla.Location(x = ego_pos[0],y = ego_pos[1],z = ego_pos[2]), carla.Rotation(yaw = ego_pos[3]))
    scenario.teleport_ego(ego_pos)


    scenario.set_stop_condition(data_reader.stop)
    # spawn_points = world.get_map().get_spawn_points()
    # for _ in range(1):
    #     point = np.random.choice(spawn_points)
    #     bp = np.random.choice(bp_lib)
    #     traffic_data.append([point, bp, True])


    recorder = DataRecorder(args, client, world, ego)


    # Start the scenario
    start = False
    while True:
        continue_sim = loop(start, scenario, recorder, args.fps)
        if not start and continue_sim:
            start = continue_sim
        if not continue_sim:
            break
    
    recorder.evaluate_metrics()
    recorder.write_log_to_file(filename = './' + args.scenario + '_log.txt', prefix = args.prefix + ' ' + str(datetime.datetime.now()))
if __name__ == '__main__':
    main()