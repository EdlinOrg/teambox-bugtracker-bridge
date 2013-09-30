# -*- coding: utf-8 -*-

"""
Synchronizes tasks from a specific task list between Teambox and Mantis

Copyright 2013 Carl Åsman http://www.edlin.org
"""

import operator
import re

import mantis_soap
import teambox


class Logic():

    def extract_mantis_id(self, str):
        match = re.search('^\(mt\:(\d+)\)', str)
        if match:
            return match.group(1)
        return False

    def has_resolved_marker(self, str):
        match = re.search('^\(mt\:resolved\)', str)
        if match:
            return True
        return False

    def teamboxtask_to_mantis_task(self, teamboxtask):
        issueData = {'project': '1',
                     'category': 'teambox_init',
                     'summary': teamboxtask['name'],
                     'description': '(teambox ' + str(teamboxtask['id']) + ')'}
        return issueData

    def add_mantis_id(self, mantis_id, text):
        return '(mt:' + str(mantis_id) + ') ' + text

    def add_teambox_id(self, teambox_id, text):
        return '(tb comment id:'+str(teambox_id) + ')\n\n' + text

    def run(self):
        teambox_obj = teambox.Teambox()
        mantis_obj = mantis_soap.MantisSoap()

        data = teambox_obj.fetchTasks()

        # loop over tasks
        for i, v in enumerate( data ):
            teambox_obj.printTask(v)

            comments = teambox_obj.fetchComments( v['id'] )
            commentObjs = sorted( comments['objects'] , key=operator.itemgetter('id') )

            #if title contains mantis id, we should update existing mantis tasks
            mantis_id = self.extract_mantis_id(v['name'])
            if mantis_id:
                print 'Found entry in mantis for teambox task id ' + str(v['id']) + '.  mantis id ' + mantis_id

                (teambox_ids_in_mantis, tocreate) = mantis_obj.getTaskNotes(mantis_id)

                #mantis ids of the notes already in teambox
                t2m_notes_transfered = []

                mantis_is_solved = mantis_obj.isSolved(mantis_id)

                #all comments from teambox, compare id and create new notes if id does not exist in mantis
                for i2, aComment in enumerate( commentObjs ):
                    #Ignore comments with empty body
                    if '' != aComment['body']:
                        extracted_mantis_id = self.extract_mantis_id(aComment['body'])

                        #check if it has mantis id, in that case we ignore it
                        if extracted_mantis_id:
                            t2m_notes_transfered.append(extracted_mantis_id)
                        else:
                            if not aComment['id'] in teambox_ids_in_mantis:
                                # check if it is a "resolved" marker that we have put there
                                if self.has_resolved_marker(aComment['body']):
                                    if mantis_is_solved:
                                        #The task has been marked as "resolved" earlier in mantis,
                                        #but someone moved it back to the task list, so we need to change the status
                                        #back to new in mantis
                                        #remove resolved status in mantis, setting it to new
                                        mantis_obj.setStatusToNew(mantis_id)
                                        pass
                                    #remove this marker from teambox
                                    teambox_obj.deleteComment(aComment['id'])
                                    mantis_is_solved = False
                                else:
                                    print 'Adding new note to mantis'
                                    mantis_obj.addNoteToTask(mantis_id,
                                                             self.add_teambox_id( aComment['id'], aComment['body']) )

                #fetch all tasks without teambox id and create those tasks in teambox
                #unless they already exist there
                for i2, aComment in enumerate( tocreate ):
                    note_id = str(aComment['id'])
                    if not note_id in t2m_notes_transfered:
                        print aComment
                        teambox_obj.createComment( str(v['id']), self.add_mantis_id(note_id, "\n\n" + teambox_obj.prepareComment(aComment) ) )

                #TODO: update existing notes if necessary, Compare update date for each comment?

                #check if status changed to "Resolved", in that case move the task from one task list to another in teambox
                if mantis_is_solved:
                    #post note that is used as place holder to know when the resolved status was set
                    teambox_obj.createComment( str(v['id']), '(mt:resolved)' )
                    teambox_obj.moveToResolved(v['id'])
            else:
                print 'Creating task in mantis for teambox id ' + str(v['id'])
                newId = mantis_obj.createTask( self.teamboxtask_to_mantis_task(v)   )
                if newId:
                    args = { 'name' : self.add_mantis_id( newId, v['name'] ) }
                    #change title of teambox task to include the id to the mantis bug
                    teambox_obj.updateTask( v['id'], args )

                #fetch all comments and create notes for all comments, sorted by id
                for i2, aComment in enumerate( commentObjs ):
                    #Ignore comments with empty body
                    if '' != aComment['body']:
                        mantis_obj.addNoteToTask(newId,
                                                 self.add_teambox_id( aComment['id'], aComment['body']) )

if __name__ == "__main__":

    obj = Logic()
    obj.run()
