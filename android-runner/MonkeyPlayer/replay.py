from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice
import sys
from com.xhaus.jyson import JysonCodec as json

def run_input(action, newdevice):
    newdevice.touch(action['x'], action['y'], 'DOWN')
    counter = (action['up'] - action['down'])/1000
    MonkeyRunner.sleep(counter)
    newdevice.touch(action['x'], action['y'], 'UP')
    print 'touch at (' + str(action['x']) + ", " + str(action['y']) + ") for " + str(counter) + " seconds"

def run_jblock(filename, newdevice):
    f = open(filename, 'r')
    print "opened file"
    for line in f:
        device_input = json.loads(line)
        run_input(device_input, newdevice)


def main():
    if len(sys.argv) == 1:
        filename = 'testLog.txt'
    else:
        filename = sys.argv[1]
    newdevice = MonkeyRunner.waitForConnection()  
    run_jblock(filename, newdevice)
    print 'done'


if __name__ == '__main__':
  main()