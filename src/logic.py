# -*- coding: utf-8 -*-

"""
Synchronizes tasks from a specific task list between Teambox and Mantis

Copyright 2013 Carl Åsman http://www.edlin.org
"""

import hashlib
import operator
import re

import config
import mantis_soap
import teambox


class Logic():

    def hash_str(self, str):
        return hashlib.sha224( str.encode('utf-8') ).hexdigest()

    def extract_mantis_id(self, str):
        match = re.search('^\(mt\:(\d+)[,\)]', str)
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
                     'description': self.teambox_create_marker( teamboxtask ) + ' ' + self.teambox_create_link(teamboxtask) }
        return issueData

    def remove_mantis_id(self, str):
        match = re.search('^\(mt\:\d+\) (.*)', str)
        if match:
            return match.group(1)
        return str

    def add_mantis_id(self, mantis_id, text):
        return '(mt:' + str(mantis_id) + ') ' + text

    def add_mantis_id_and_name(self, mantis_id, user_info, text):
        return '(mt:' + str(mantis_id) + ', ' + user_info + ' - hash:' + self.hash_str( text ) + ')'

    def add_mantis_info_and_format(self, mantis_id, aComment):
        tmp = self.add_mantis_id_and_name( mantis_id,
                                           self.mantis_obj.extractUserInfoFromNote( aComment ),
                                           aComment['text'] )
        return tmp + "\n\n" + self.teambox_obj.prepareComment(aComment)

    def add_teambox_id(self, comment):
        text = comment['body']
        user_info = self.teambox_user_info( comment['user_id'] )
        return self.teambox_create_marker( comment, self.hash_str( text ) ) + '\n\n' + text

    def extract_hash_from_mantis(self, mantis_str):
        match = re.search('^\(tb\:\d+, .* - hash\:([\d\w]*)\)', mantis_str)
        if match:
            return match.group(1)
        return ''

    def extract_hash_from_teambox(self, tb_str):
        match = re.search('^\(mt\:\d+, .* - hash\:([\d\w]*)\)', tb_str)
        if match:
            return match.group(1)
        return ''

    def teambox_create_marker(self, aTaskOrComment, hash=False):
        user_info = self.teambox_user_info( aTaskOrComment['user_id'] )
        if hash:
            user_info += ' - hash:' + hash
        return '(tb:'+str( aTaskOrComment['id'] ) + ', ' + user_info + ')'

    def teambox_user_info(self, user_id):
        data = self.teambox_obj.getUser( user_id )
        return data['first_name'] + ' ' + data['last_name']

    def teambox_create_link(self, teamboxtask):
        return 'https://teambox.com/#!/projects/' + str( self.teambox_obj.teambox_projectid ) + '/tasks/' + str(teamboxtask['id'])

    def run(self):
        mantis_obj = mantis_soap.MantisSoap()
        self.mantis_obj = mantis_obj

        buglists = config.TEAMBOX_TASKLISTS

        for tasklist_id in buglists:

            teambox_obj = teambox.Teambox(tasklist_id)
            self.teambox_obj = teambox_obj

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
    
                    mantisTask = mantis_obj.getTask(mantis_id)
    
                    #Check if title changed
                    tmpName = mantisTask['summary']
                    tmpName2 = self.remove_mantis_id( v['name'] )
                    if tmpName != tmpName2:
                        # title of bug has been changed,
                        # Teambox is master and change title in mantis
                        print "Updating summary in Mantis"
                        mantisTask['summary'] = tmpName2
                        mantisTask['notes'] = []  # prevent update of all notes attached
                        mantis_obj.updateTask( mantis_id, mantisTask )

                    (teambox_ids_in_mantis, tocreate) = mantis_obj.getTaskNotes(mantis_id)

                    #mantis ids of the notes already in teambox
                    t2m_notes_transfered = []

                    mantis_is_solved = mantis_obj.isSolved(mantis_id)

                    mantis_notes_to_update = []

                    #all comments from teambox, compare id and create new notes if id does not exist in mantis
                    for i2, aComment in enumerate( commentObjs ):
                        #Ignore comments with empty body
                        if '' != aComment['body']:
                            extracted_mantis_id = self.extract_mantis_id(aComment['body'])

                            #check if it has mantis id, in that case we ignore it
                            if extracted_mantis_id:
                                #check if it has been updated in mantis, in that case overwrite in tb
                                theNote = mantis_obj.getTaskNoteByNoteId(mantis_id, extracted_mantis_id)
                                if False != theNote:
                                    teambox_hash = self.extract_hash_from_teambox( aComment['body'] )
                                    mantis_hash = self.hash_str( theNote['text'] )
                                    if mantis_hash != teambox_hash:
                                        print "Hashes do not match, will update Teambox note"
                                        teambox_obj.updateComment( str( aComment['id'] ),
                                                                   self.add_mantis_info_and_format( extracted_mantis_id, theNote )
                                                                   )

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
                                                                 self.add_teambox_id( aComment ) )
                                else:
                                    #check if it was updated in teambox, in that case overwrite in mantis
                                    theNote = mantis_obj.getTaskNoteByTbId(mantis_id, aComment['id'])
                                    if theNote:
                                        #compare hash
                                        mantis_hash = self.extract_hash_from_mantis( theNote['text'] )
                                        teambox_hash = self.hash_str( aComment['body'] )
                                        if mantis_hash != teambox_hash:
                                            aNote = {
                                                        'taskid': theNote['id'],
                                                        'note':  self.add_teambox_id( aComment )
                                                    }
                                            mantis_notes_to_update.append(aNote)
                                            print "Will update note in mantis, id: " + str( theNote['id'] )

                    for aNote in mantis_notes_to_update:
                        mantisTask = mantis_obj.getTask(mantis_id)
                        tmparr = []
                        for existingNote in mantisTask['notes'] :
                            if existingNote['id'] == aNote['taskid']:
                                existingNote['text'] = aNote['note']
                                tmparr.append(existingNote)
                        mantisTask['notes'] = tmparr
                        mantis_obj.updateTask( mantis_id, mantisTask )

                    #fetch all notes without teambox id and create those tasks in teambox
                    #unless they already exist there
                    for i2, aComment in enumerate( tocreate ):
                        note_id = str(aComment['id'])
                        if not note_id in t2m_notes_transfered:
                            print "Creating a note in Teambox"
                            teambox_obj.createComment( str(v['id']), self.add_mantis_info_and_format(note_id, aComment) )

                    #check if status changed to "Resolved", in that case move the task from one task list to another in teambox
                    if mantis_is_solved:
                        #post note that is used as place holder to know when the resolved status was set
                        teambox_obj.createComment( str(v['id']), '(mt:resolved)' )
                        teambox_obj.moveToResolved(v['id'])
                else:
                    print 'Creating task in mantis for teambox id ' + str(v['id'])
                    newId = mantis_obj.createTask( self.teamboxtask_to_mantis_task(v) )
                    if newId:
                        args = { 'name' : self.add_mantis_id( newId, v['name'] ) }
                        #change title of teambox task to include the id to the mantis bug
                        teambox_obj.updateTask( v['id'], args )
                    else:
                        print "Error: failed creating task in mantis"

                    #fetch all comments and create notes for all comments, sorted by id
                    for i2, aComment in enumerate( commentObjs ):
                        #Ignore comments with empty body
                        if '' != aComment['body']:
                            mantis_obj.addNoteToTask(newId,
                                                     self.add_teambox_id( aComment ) )

if __name__ == "__main__":

    obj = Logic()
    obj.run()
