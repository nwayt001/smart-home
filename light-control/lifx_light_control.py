from lifxlan import LifxLAN
import time
from piclap import *

'''
# Base light controller for the lifx brand smart light

 current implementation works only with a single light
 TODO: add multi-light support
'''
class LifxLightController(object):
    # Initialize and connect to lights
    def __init__(self, debug = True):

        print('Initializing Light Control..')
        self.debug = debug
        self.MAX_CONNECTION_RETRIES = 5
        self.toggle_light = False
        self.lifx = LifxLAN(1)
        print("Connecting...")

        self.light = None
        for i in range(self.MAX_CONNECTION_RETRIES):
            try:
                # get lights
                #devices = Lifx.get_lights()
                #light = devices[0]
                self.light = self.lifx.get_device_by_name("mini_1")
                break
            except:
                print("Retrying...")
                time.sleep(1)

        if self.light is None:
            raise Exception("Failed to connect to LIFX device! Please try again.")

        print("Connected!")
    
        # get original settings
        self.original_power = self.light.get_power()
        self.original_color = self.light.get_color()

        if self.debug:
            print(self.original_power)
            print(self.original_color)


    # toggle lights
    def toggle_lights(self):
        self.toggle_light = not self.toggle_light
        if self.toggle_light:
            self.light.set_power("on")
        else:
            self.light.set_power("off")

# Class to control lifx lights using a clap detector
class ClapController(LifxLightController):
    def __init__(self, debug=True):
        # Initialize base class
        super(ClapController, self).__init__(debug)

        # Initialize clap detector using piclap
        self.options = self.PiClapOptions(debug, self)

        self.listener = Listener(config = self.options, calibrate = False)
        self.listener.start()

    class PiClapOptions(Settings):
        # custom settings for pi-clap

        def __init__(self, debug, controller):
            Settings.__init__(self)
            self.controller = controller
            self.method.value=10000 # calibrate

        def on2Claps(self):
            self.controller.toggle_lights()
            print("Detected 2 claps")

        def on3Claps(self):
            print("Detected 3 claps")
            self.controller.toggle_lights()

        def on4Claps(self):
            print("detected 4 claps")
            self.controller.toggle_lights()
            
if __name__ == '__main__':
    clapper = ClapController(debug = True)