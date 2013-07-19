import unittest

import logic

class LogicTest(unittest.TestCase):

    def test_extract_mantis_id(self):
        obj = logic.Logic()

        self.assertEqual(False, obj.extract_mantis_id('Apa bepa cepa') )
        self.assertEqual(False, obj.extract_mantis_id('donkey (mt:123) Apa bepa cepa') )
        self.assertEqual('123', obj.extract_mantis_id('(mt:123) Apa bepa cepa') )

        apa = obj.add_mantis_id('123','apa bepa')
        self.assertEqual('123', obj.extract_mantis_id( apa ) )

    def test_add_mantis_id(self):
        obj = logic.Logic()
        self.assertEqual('(mt:a) b', obj.add_mantis_id('a','b') ) 

    def test_teamboxtask_to_mantis_task(self):
        obj = logic.Logic()
        args = { 'id': 123, 'name' : 'apa bepa' }
        self.assertEqual( {'project': '1', 'category': 'teambox_init', 'description': '(teambox 123)', 'summary': 'apa bepa'},  obj.teamboxtask_to_mantis_task(args) ) 

if __name__ == '__main__':
    unittest.main()

