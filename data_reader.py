import xml.etree.ElementTree as ET

class DataReader():
    def __init__(self):
        self.file = None
        self.actors = []
        self.ego = None
        self.stop = None
    def read_data(self, filename):
        self.file = ET.parse(filename)
        if self.file is None:
            print('Error openning xml file')
            return False
        
        root = self.file.getroot()
        if root is None:
            print('Error finding root in xml file')
            return False
        
        traffic = root.find('traffic')
        if traffic is None:
            print('No traffic found in xml file')
            return False
        
        id = 0
        for actor in traffic:
            actor_id = actor.attrib.get('id')
            if actor_id is None:
                actor_id = id
            else:
                actor_id = int(actor_id)

            position = actor.find('position')
            rotation = actor.find('rotation')
            autopilot = actor.attrib.get('autopilot')

            if position is None or rotation is None:
                print('Error getting actor {} initial state'.format(actor_id))
                continue

            x = position.find('x')
            y = position.find('y')
            z = position.find('z')
            yaw = rotation.find('yaw')
            if x is None or y is None or yaw is None:
                print('Error getting actor {} initial state'.format(actor_id))
                continue
            else:
                x = float(x.text)
                y = float(y.text)
                yaw = float(yaw.text)

            if z is None:
                z = 0.3
            else:
                z = float(z.text)

            if autopilot is None:
                autopilot = True
            else:
                autopilot = True if autopilot=='1' else False

            self.actors.append([actor_id, (x,y,z,yaw), autopilot])
            id += 1

        ego = root.find('ego')
        if ego is None:
            print('No ego vehicle provided')

        position = ego.find('position')
        rotation = ego.find('rotation')

        if position is None or rotation is None:
            print('Error getting ego initial state')
        else:
            x = position.find('x')
            y = position.find('y')
            z = position.find('z')
            yaw = rotation.find('yaw')
            if x is None or y is None or yaw is None:
                print('Error getting ego initial state')
            else:
                x = float(x.text)
                y = float(y.text)
                yaw = float(yaw.text)

            if z is None:
                z = 0.3
            else:
                z = float(z.text)
        self.ego = [x,y,z,yaw]

        stop = root.find('stop')
        if stop is None:
            print('No stop condition provided')

        position = stop.find('position')
        rotation = stop.find('rotation')

        if position is None or rotation is None:
            print('Error getting stop condition state')
        else:
            x = position.find('x')
            y = position.find('y')
            z = position.find('z')
            yaw = rotation.find('yaw')
            if x is None or y is None or yaw is None:
                print('Error getting stop condition state')
            else:
                x = float(x.text)
                y = float(y.text)
                yaw = float(yaw.text)

            if z is None:
                z = 0.3
            else:
                z = float(z.text)
        self.stop = [x,y,z,yaw]
        return True

    def get_actors(self):
        return self.actors

    def get_ego(self):
        return self.ego