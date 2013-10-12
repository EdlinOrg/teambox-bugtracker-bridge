import unittest

import json
import pprint

import teambox

#export PYTHONPATH="../src:$PYTHONPATH"


class TeamboxTest(unittest.TestCase):

    def setUp(self):
        self.obj = teambox.Teambox()

#    def test_prepareComment(self):
#        url = 'https://teambox.com/#!/search/mt%3A'
#
#        arr = {'text' : 'apa', 'reporter' : {'name' : 'dilbert'} }
#        self.assertEqual("dilbert:\napa", self.obj.prepareComment( arr ) )
#
#        arr = {'text' : 'apa #34 bepa', 'reporter' : {'name' : 'dilbert'} }
#        expected = 'dilbert:\napa #34 (' + url + '34) bepa'
#        self.assertEqual(expected, self.obj.prepareComment( arr ) )
#
#        arr = {'text' : '#12a', 'reporter' : {'name' : 'dilbert'} }
#        self.assertEqual('dilbert:\n#12a', self.obj.prepareComment( arr ) )

#    def test_deleteComment(self):
#        self.obj.deleteComment('17301353')

#    def test_getTeamboxImportedTasks(self):
#        self.obj.getTeamboxImportedTasks()

#    def test_updateTask(self):
#        args = { 'name' : '(mt:6666) update of task from python' }
#        self.obj.updateTask(4919082, args)

#    def test_getTask(self):
#        data = self.obj.getTask(4919082)
#        print data

#    def test_moveToResolved(self):
#        self.obj.moveToResolved(4918910)

    def test_fetchComments(self):
        data = self.obj.fetchComments(5372110)
        print data
        for i, v in enumerate( data['objects'] ):
            print 'INDENT:', json.dumps(v, sort_keys=True, indent=2)

    def test_updateComment(self):
        self.obj.updateComment(16953889, 'UPdateekj')
        #16953889

#    def test_fetchTasks(self):
#        data = self.obj.fetchTasks()
#        print 'INDENT:', json.dumps(data, sort_keys=True, indent=2)

#    def test_getUser(self):

#        data = self.obj.getUser(677491)
#        print data['last_name']
#        data = self.obj.getUser(677491)
#        print data['first_name']
#        pprint.pprint(data)


if __name__ == '__main__':
    unittest.main()
