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
Synchronizes tasks from specific task lists between Teambox and bugtrackers (currently Mantis is implemented).

See

http://www.edlin.org/software-development/teambox-bugtracker-bridge.html

for screenshots what it looks like in action.

The files:

* config.py      - config data (url:s, login data for teambox / mantis etc)
* logic.py       - the main file, should be called as a cron job reguarly to perform the sync.
* teambox.py     - the interface to Teambox, uses their REST interface
* mantis_soap.py - the interface to Mantis, uses the SOAP interface mantisconnect

It is recommended that you setup one virtual user in Teambox and one virtual user in Mantis
that are the users defined in config.py.

The tasks will then be created as these virtual users and it is obvious that it was not a "real" user that created the tasks / notes.


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

For each comment that has been transferred to/from Mantis, the comment in Teambox is prepended with
"(mt:XXXXX, YYYY - hash:ZZZ)"

where
* XXXX is the id of the correpsonding note in Mantis
* AAAA is the name of the user in Mantis (either fullname, or not available, the username)
* ZZZ is the a calculated hash of the text in mantis. This hash is used to determine if a note has been updated

When a task is marked as completed in mantis, a comment is added to that task in Teambox, with the content
"(mt:resolved)", and then task is moved to the "resolved" task list.

Markers in Mantisbt:

In the "Description" field in mantis,
the teambox id is saved as "(tb:XXXXX, YYYY)" where XXXXX is the Teambox id
and YYYY is the users name in Teambox

Comments that were synchronized from Teambox:
The Mantis "Note" start with "(tb:XXXXX, YYYY - hash:ZZZ)"

where
* XXXXX is the corresponding comment id in Teambox
* YYYY is the users name in Teambox
* ZZZ is the a calculated hash of the text in mantis. This hash is used to determine if a note has been updated

Misc notes
----------
* If a task is deleted in Teambox, nothing happens in mantis (the task remains there)
* If a task is deleted in Mantis, the task from Teambox will be copied over to Mantis with the next sync.
* If a task title was changed in Teambox, the title will be updated in Mantis
* If a title was changed in Mantis, it will be overwritten with the task title from Teambox with next sync
* If the pattern " #DDD " (where DDD are any amount of digits) is found in a Mantis note, it is assumed to be a reference to a different
Mantis task, and we will create an url in Teambox which searches Teambox for this task using the searchquery "mt:DDD"
