import unittest

import json

import teambox

#export PYTHONPATH="../src:$PYTHONPATH"

class TeamboxTest(unittest.TestCase):

    def setUp(self):
        self.obj = teambox.Teambox()

#    def test_getTeamboxImportedTasks(self):
#        self.obj.getTeamboxImportedTasks()

#    def test_updateTask(self):
#        args = { 'name' : '(mt:6666) update of task from python' }
#        self.obj.updateTask(4919082, args)

#    def test_getTask(self):
#        data = self.obj.getTask(4919082)
#        print data

#    def test_moveToResolved(self):
#        self.obj.moveToResolved(4919082)

#    def test_fetchComments(self):
#        data = self.obj.fetchComments(4911022)
#        for i, v in enumerate( data['objects'] ):
#            print 'INDENT:', json.dumps(v, sort_keys=True, indent=2)

#    def test_fetchTasks(self):
#        data = self.obj.fetchTasks()
#        print 'INDENT:', json.dumps(data, sort_keys=True, indent=2)

if __name__ == '__main__':
    unittest.main()

