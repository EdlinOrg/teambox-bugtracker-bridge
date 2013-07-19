import unittest

import mantis_soap

class MantisSoapTest(unittest.TestCase):

    def setUp(self):
        self.obj = mantis_soap.MantisSoap()

#    def test_getTeamboxImportedTasks(self):
#        apa = self.obj.getTeamboxImportedTasks()
#        print apa

#    def test_createTask(self):
#        issueData = {'project' : '1' , 'category' : 'teambox_init', 'summary' : 'python adding.....' , 'description' : 'with a description'}
#        self.obj.createTask( issueData )


#    def test_updateTask(self):
#        issueData = {'project' : '1' , 'category' : 'teambox_init', 'summary' : 'a b c d e ITS AN UPDATE...' , 'description' : 'f g h YEAH'}
#        self.obj.updateTask( 82, issueData )

#    def test_addNoteToTask(self):
#         self.obj.addNoteToTask(21, 'it is a note from python')

#    def test_getTask(self):
#         data = self.obj.getTask(80)
#         print data
#         print self.obj.isSolved(82)

#    def test_getTaskNotesTeamboxIds(self):
#        data = self.obj.getTaskNotesTeamboxIds(82)
#        print data

#    def test_extractTeamboxIdFromNote(self):
#        self.assertEqual(False,self.obj.extractTeamboxIdFromNote('Apa bepa cepa') )
#        self.assertEqual(False,self.obj.extractTeamboxIdFromNote('epa (tb comment id:5432)\n\nApa bepa cepa') )
#        self.assertEqual('5432',self.obj.extractTeamboxIdFromNote('(tb comment id:5432)\n\nApa bepa cepa') )

if __name__ == '__main__':
    unittest.main()

