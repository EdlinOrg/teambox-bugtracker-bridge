
from suds.client import Client
import re

import config

#debug for developing
#import logging
#logging.basicConfig(level=logging.DEBUG, filename="suds.log")
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

class MantisSoap():

    def __init__(self):
        self.url = config.MANTIS_SOAPURL
        self.wdsl = config.MANTIS_SOAP_WDSL

        self.username = config.MANTIS_USERNAME
        self.password = config.MANTIS_PASSWORD

        self.server = Client(url=self.wdsl, location=self.url).service;

        self.cached_mantis_obj=False

    def extractTeamboxIdFromNote(self,str):
        """ Extract the teambox id from the string
            Looks for (tb comment id:NNN+} at the beginning of the string

        Parameters
        ----------
        str : string

        Returns
        -------
        string
            The id as a string
        boolean
            False if no id found
        """
        match = re.search('^\(tb comment id\:(\d+)\)\n\n', str)
        if match:
            return match.group(1)
        return False

    def getTaskNotesTeamboxIds(self, mantis_id):
        """ return all the teambox ids for the notes """

        data = self.getTask(mantis_id)

        l = []
        for i2, aComment in enumerate( data['notes'] ):
            teambox_id = self.extractTeamboxIdFromNote(aComment['text'])
            if teambox_id:
                l.append( int(teambox_id) )
        return l

    def getTaskNotes(self, mantis_id):
        data = self.getTask(mantis_id)

        l = []
        a = []
        for i2, aComment in enumerate( data['notes'] ):
            teambox_id = self.extractTeamboxIdFromNote(aComment['text'])
            if teambox_id:
                l.append( int(teambox_id) )
            else:
                a.append(aComment)
        return (l,a)

    def getTask(self, mantis_id):
        if self.cached_mantis_obj and self.cached_mantis_obj['id'] == mantis_id:
            return self.cached_mantis_obj
        else:
            self.cached_mantis_obj = self.server.mc_issue_get( self.username, self.password, mantis_id ) 
        return self.cached_mantis_obj

    def addNoteToTask(self, task_id, note):
        data = { 'text' : note }
        self.server.mc_issue_note_add( self.username, self.password, task_id, data ) 

    def createTask(self, task):
        newid = self.server.mc_issue_add(username=self.username, password=self.password, issue=task)        
        print "Success: issue %s created" % newid
        return newid

    def updateTask(self, issue_id, task):
        self.server.mc_issue_update(username=self.username, password=self.password, issueId= issue_id, issue=task)        

    def isSolved(self, issue_id):
        #80 = resolved
        task = self.getTask(issue_id)
        return task['status']['id'] == 80
