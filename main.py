import argparse
import xml.etree.ElementTree as ET

from scenario import Scenario

def run_scenario(**kwargs): # TODO: add scenario creation, check parameters
    # We create scenarion and starts it
    #scenario = Scenario()
    pass
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=None, type=str,
                        help='Path to config file')
    args = parser.parse_args()
    if args.config:
        config_file = ET.parse(args.config)
        kwargs = {}
        for item in config_file.getroot():
            kwargs[item.tag] = item.text
        run_scenario(**kwargs)
    else:
        print('No config file provided!')
        pass