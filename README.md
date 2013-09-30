Shameless self-plugging
-----------------------
I am a freelancing software developer (M.Sc.) that has been working fulltime for over 15 years now in various fields

See

http://www.edlin.org/

for info on my background. Please feel free to contact me if you are looking for developers.
I prefer to work remotely on projects.

That said, let's carry on with some notes about this code:

teambox-bugtracker-bridge
=========================
Synchronizes tasks from a specific task list between Teambox and bugtrackers (currently Mantis is implemented).

See

http://www.edlin.org/software-development/teambox-bugtracker-bridge.html

for screenshots what it looks like in action.

The files:

* config.py      - config data (url:s, login data for teambox / mantis etc)
* logic.py       - the main file, should be called as a cron job reguarly to   perform the sync.
* teambox.py     - the interface to Teambox, uses their REST interface
* mantis_soap.py - the interface to Mantis, uses the SOAP interface mantisconnect


The websites for Teambox & Mantis:

* http://teambox.com/
* http://www.mantisbt.org/

Markers
-------

To keep track of statuses and what has been transferred, this meta info are saved in mantis/teambox
(rather than a separate db)

Markers in Teambox:

When a task has been transferred to mantis, the title of the Teambox task is prepended with "(mt:XXXXX)"
where XXXXX is the id of the corresponding task in Mantis

For each comment that has been transferred to/from Mantis, the comment in Teambox is prepended with "(mt:XXXXX)"
where XXXX is the id of the correpsonding note in Mantis

When a task is marked as completed in mantis, a comment is added to that task in Teambox, with the content
"(mt:resolved)", and then task is moved to the "resolved" task list.

Markers in Mantisbt:

In the "Description" field in mantis,
the teambox id is saved as "(teambox XXXXX)" where XXXXX is the Teambox id

Comments that were synchronized from Teambox:
The Mantis "Note" start with "(tb comment id:XXXXX)"
where XXXXX is the corresponding comment id in Teambox

