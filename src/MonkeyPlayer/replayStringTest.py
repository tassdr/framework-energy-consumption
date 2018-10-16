#from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
from com.xhaus.jyson import JysonCodec as json

def run_input(action):
    #newdevice.touch(action['x'], action['y'], DOWN)
    counter = action['up'] - action['down']
    #time.sleep(counter)
    #newdevice.touch(action['x'], action['y'], UP)
    print 'touch at (' + str(action['x']) + ", " + str(action['y']) + ") for " + str(counter) + " seconds"

def run_jblock(filename):
    f = open(filename, 'r')
    for line in f:
        device_input = json.loads(line)
        run_input(device_input)

def main():
    if len(sys.argv) != 2:
        print 'usage: ./replay.py file'
        sys.exit(1)
    filename = sys.argv[1]
    #newdevice = MonkeyRunner.waitForConnection()  
    #deviceAC = build_jblock(filename)
    run_jblock(filename)


if __name__ == '__main__':
  main()