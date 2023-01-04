import argparse
import glob
import math
import numpy as np
import os
import sys
import time
from state import State
from metrics.AOL_metric import AOLMetric
from metrics.max_curvature_metric import MaxCurvatureMetric
from metrics.path_length_metric import PathLengthMetric
from metrics.normalized_curvature_metric import NormalizedCurvatureMetric
from metrics.time_metric import TimeMetric
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla 

class DataRecorder():
    def __init__(self, args, client, world, vehicle):
        self.log = []
        self.client = client
        self.world = world
        self.vehicle = vehicle
        self.FPS = args.fps if args.fps is not None else 30
        self.metrics = [TimeMetric,
                        PathLengthMetric,
                        AOLMetric,
                        MaxCurvatureMetric,
                        NormalizedCurvatureMetric]
        self.results = {}

    def connect(self, args):
        self.client = carla.Client(args.host, args.port)
        if args.timeout:
            self.client_timeout = args.timeout
        self.client.set_timeout(self.client_timeout)
        
        self.world = self.client.get_world()
        actors = self.world.get_actors().filter('*vehicle*')
        print(actors)
        if len(actors) == 0:
            print('No active vehicle was found. Abort')
            raise ValueError
        else:
            self.vehicle = actors[len(actors)-1]
        # if self.client is None:
        #     print('Cannot connect to carla client')
        #     raise ModuleNotFoundError
    
    def record(self):
        t = self.vehicle.get_transform()
        v = self.vehicle.get_velocity()
        # c = vehicle.get_control()
        # a = vehicle.get_acceleration()
        # av = vehicle.get_angular_velocity()
        snapshot = self.world.get_snapshot()
        state = np.array([snapshot.timestamp.elapsed_seconds, t.location.x, -t.location.y, math.radians(-t.rotation.yaw), math.sqrt(v.x**2 + v.y**2 + v.z**2)])
        self.log.append(state)
        time.sleep(1/self.FPS)
        return state

    def get_vehicle_position(self):
        t = self.vehicle.get_transform()
        v = self.vehicle.get_velocity()
        snapshot = self.world.get_snapshot()
        state = np.array([snapshot.timestamp.elapsed_seconds, t.location.x, -t.location.y, math.radians(-t.rotation.yaw), math.sqrt(v.x**2 + v.y**2 + v.z**2)])
        return state

    def record_one_time(self):
        state = self.get_vehicle_position()
        self.log.append(state)
        return state
        
    def evaluate_metrics(self, **kwargs):
        adapted_path = []
        for carla_state in self.log:
            s = State(x = carla_state[1], y = carla_state[2], theta=carla_state[3], timestamp = carla_state[0])
            adapted_path.append(s)
        self.results.clear()
        for metric in self.metrics:
            result = metric.evaluate_metric(adapted_path, **kwargs)
            self.results[metric.__name__] = result
            print('Result for metric {} is {}'.format(metric.__name__,result))

    def print_data(self):
        print('Path and speed of ego-vehicle is:')
        for state in self.log:
            print(state)

    def write_log_to_file(self, filename, prefix):
        with open(filename, "a") as logfile:
            logfile.write('{} - '.format(prefix))
            for metric, value in self.results.items():
                logfile.write('{}({}); '.format(metric, value))
            logfile.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost',
                    help='IP of the host server (default: localhost)')
    parser.add_argument('--port', default=2000, type=int,
                    help='TCP port to listen to (default: 2000)')
    parser.add_argument('--fps', default=30, type=int,
                    help='Rate at which recorder will record data')
    parser.add_argument('--timeout', default=300.0, type=float,
                    help='Set the CARLA client timeout value in seconds')
    args = parser.parse_args()

    client = carla.Client(args.host, args.port)
    if args.timeout:
        client.set_timeout(args.timeout)
    world = client.get_world()
    actors = world.get_actors().filter('*vehicle*')
    ego_vehicle = actors[0]

    recorder = DataRecorder(args, client, world, ego_vehicle)
    print('Recorder created and connected')
    begin = time.time()
    try:
        while True:
            r = recorder.record()
            print(r)
    except KeyboardInterrupt:
        print('End of recording')
    except Exception as e:
        print('Some exception happend')
        print(e)
    finally:
        recorder.evaluate_metrics()
        print('Metrics calculated')
        #recorder.print_data()
    
