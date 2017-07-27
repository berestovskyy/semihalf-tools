Set up Python

Please consult the Spirent TestCenter Base and Test Package Release Notes for supported versions of Python. Release notes are included on the DVD and are available as a "Related Resource" on each software download page (http://support.spirent.com). 

To set up Python to run with Spirent TestCenter:

1 Copy StcPython.py to your scripts directory.
2 Open StcPython.py for editing and modify the following line to point to your
   Spirent TestCenter installation directory, or optionally set the system environment variable.

   os.environ['STC_PRIVATE_INSTALL_DIR'] = STC_PRIVATE_INSTALL_DIR

Verify the set up:

1  cd to your scripts directory.

2  Type python at the command line and press Enter.
    The Python interpreter starts.

3  Type from StcPython import StcPython and press Enter.

4  Type stc = StcPython()and press enter.

5  Type print stc.get('system1', 'version')and press Enter.
    The Spirent TestCenter version will display.

Python is ready to be used with Spirent TestCenter Automation.