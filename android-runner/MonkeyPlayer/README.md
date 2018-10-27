MonkeyRunner - Android Record and Replay UI Testing Framework
========================

Developed for COMS 6998 - Cloud and Mobile Security Seminar - Columbia University - Spring 2013

Abstract—We have developed a user interface driven record and replay system for the Android mobile operating system. By modifying the Android View application programming interface we are able to log interactions within the system to be replayed at a later time using a tool built on top of Googles provided MonkeyRunner framework. This type of user interface replay is useful for testing and debugging as well as more novel applications like system auditing.

A modified android kernel is needed to needed to capture the touch input and create the log. It is not included here due to the size.

download jyson from here: http://downloads.xhaus.com/jyson/
place the .jar file in your directory so they JSON parsing in the monkeyrunner python scripts run correctly

to run replay:
monkeyrunner -plugin jyson.jar replayLogic.py logfilename.txt

-tag is to include the plug in for JSON
- by default the script looks for testLogicLog.txt if no filename is specified
