teambox-bugtracker-bridge
=========================

Synchronizes tasks from a specific task list between Teambox and bugtrackers (currently Mantis is implemented).

See
http://www.edlin.org/software-development/teambox-bugtracker-bridge.html
for screenshots what it looks like in action.

config.py      - config data (url:s, login data for teambox / mantis etc)
logic.py       - the main file, should be called as a cron job reguarly to perform the sync.
teambox.py     - the interface to Teambox, uses their REST interface
mantis_soap.py - the interface to Mantis, uses the SOAP interface mantisconnect


The websites for Teambox & Mantis:
http://teambox.com/
http://www.mantisbt.org/
