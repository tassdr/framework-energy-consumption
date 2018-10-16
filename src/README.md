# Android Task runner
Automated experiment execution on Android devices

## Install
This tool is only tested on Ubuntu, but it should work in other linux distributions.
You'll need:
- Python 2.7
- Android Debug Bridge (`sudo apt install android-tools-adb`)
- Android SDK Tools (`sudo apt install monkeyrunner`)
- JDK 8 (NOT JDK 9) (`sudo apt install openjdk-8-jre`)
- lxml (`sudo apt install python-lxml`)

Additionally, the following are also required for the Batterystats method:
- power_profile.xml (retrievable from the device using [APKTool](https://github.com/iBotPeaches/Apktool))
- systrace.py (from the Android SDK Tools)
- A device that is able to report on the `idle` and `frequency` states of the CPU using systrace.py

Note: It is important that monkeyrunner shares the same adb the experiment is using. Otherwise, there will be an adb restart and output may be tainted by the notification.

Note 2: You can specifiy the path to ADB and/or Monkeyrunner in the experiment configuration. See the Experiment Configuration section below.

Note 3: To check whether the the device is able to report on the `idle` and `frequency` states of the CPU, you can run the command `python systrace.py -l` and ensure both categories are listed among the supported categories.

## Quick start
To run an experiment, run:
```bash
python android_runner your_config.json
```
Example configuration files can be found in the subdirectories of the `example` directory.

## Structure
### devices.json
A JSON config that maps devices names to their ADB ids for easy reference in config files.

### Experiment Configuration
Below is a reference to the fields for the experiment configuration. It is not always updated.

**adb_path** *string*
Path to ADB. Example path: `/opt/platform-tools/adb`

**monkeyrunner_path** *string*
Path to Monkeyrunner. Example path: `/opt/platform-tools/bin/monkeyrunner`

**systrace_path** *string*
Path to Systrace.py. Example path: `/home/user/Android/Sdk/platform-tools/systrace/systrace.py`

**powerprofile_path** *string*
Path to power_profile.xml. Example path: `android-runner/example/batterystats/power_profile.xml`

**type** *string*
Type of the experiment. Can be `web` or `native`

**replications** *positive integer*
Number of times an experiment is run.

**duration** *positive integer*
The duration of each run in milliseconds.

**devices** *Array\<String\>*
The names of devices to use. They will be translated into ids defined in devices.json.

**paths** *Array\<String\>*
The paths to the APKs/URLs to test with.

**browsers** *Array\<String\>*
*Dependent on type = web*
The names of browser(s) to use. Currently supported values are `chrome`.

**profilers** *JSON*
A JSON object to describe the profilers to be used and their arguments. Below are several examples:
```json
  "profilers": {
    "trepn": {
      "sample_interval": 100,
      "data_points": ["battery_power", "mem_usage"]
    }
  }
```

```json
  "profilers": {
    "android": {
      "sample_interval": 100,
      "data_points": ["cpu", "mem"]
    }
  }
```

```json
  "profilers": {
    "batterystats": {
      "cleanup": true
    }
  }
```

**cleanup** *boolean*
Delete log files required by Batterystats after completion of the experiment. The default is *true*.

**scripts** *JSON*
A JSON list of types and paths of scripts to run. Below is an example:
```json
"scripts": {
  "before_experiment": "before_experiment.py",
  "before_run": "before_run.py",
  "interaction": "interaction.py",
  "after_run": "after_run.py",
  "after_experiment": "after_experiment.py"
}
```
Below are the supported types:
- before_experiment
  executes once before the first run
- before_run
  executes before every run
- after_launch
  executes after the target app/website is launched, but before profiling starts
- interaction
  executes between the start and end of a run
- after_run
  executes after a run completes
- after_experiment
  executes once after the last run

## Detailed documentation
The original thesis can be found here:
https://drive.google.com/file/d/0B7Fel9yGl5-xc2lEWmNVYkU5d2c/view?usp=sharing

The thesis regarding the implementation of Batterystats can be found here:
https://drive.google.com/file/d/1O7BqmkRFRDq7AD1oKOGjHqJzCTEe8AMz/view?usp=sharing

## FAQ
### Devices have no permissions (udev requires plugdev group membership)
This happens when the user calling adb is not in the plugdev group.
#### Fix
`sudo usermod -aG plugdev $LOGNAME`
#### References
https://developer.android.com/studio/run/device.html

http://www.janosgyerik.com/adding-udev-rules-for-usb-debugging-android-devices/

### [Batterystats] IOError: Unable to get atrace data. Did you forget adb root?
This happens when the device is unable to retrieve CPU information using systrace.py.
#### Fix
Check whether the device is able to report on both categories `freq` and `idle` using Systrace:

`python systrace.py -l`

If the categories are not listed, use a different device.
#### References
https://developer.android.com/studio/command-line/systrace
