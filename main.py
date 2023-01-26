import argparse
import xml.etree.ElementTree as ET

from scenario import Scenario

def run_scenario(**kwargs): # TODO: add scenario creation, check parameters
    # We create scenarion and starts it
    scenario = Scenario(**kwargs)
    if not scenario.load_scenario():
        return False
    if not scenario.prepare_scenario():
        return False
    
    while True:
        if not scenario.sim_loop():
            break
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=None, type=str,
                        help='Path to config file', required=True)
    parser.add_argument('--scenario', default=None, type=str,
                        help='[Optional] Scenario to choose. Overrides scenario in config file', required=False)
    args = parser.parse_args()
    
    if args.config is None:
        print('No config file provided!')
        pass
    
    config_file = ET.parse(args.config)
    kwargs = {}
    for item in config_file.getroot():
        kwargs[item.tag] = item.text
    
    if args.scenario is not None:
        kwargs['scenario'] = args.scenario
    
    if run_scenario(**kwargs):
        print('Success!')