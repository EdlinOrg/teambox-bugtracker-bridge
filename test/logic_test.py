import unittest

import logic


class LogicTest(unittest.TestCase):

    def test_extract_mantis_id(self):
        obj = logic.Logic()

        self.assertEqual(False, obj.extract_mantis_id('Apa bepa cepa') )
        self.assertEqual(False, obj.extract_mantis_id('donkey (mt:123) Apa bepa cepa') )
        self.assertEqual('123', obj.extract_mantis_id('(mt:123) Apa bepa cepa') )

        apa = obj.add_mantis_id('123', 'apa bepa')
        self.assertEqual('123', obj.extract_mantis_id( apa ) )

    def test_has_resolved_marker(self):
        obj = logic.Logic()
        self.assertTrue( obj.has_resolved_marker('(mt:resolved)') )
        self.assertFalse( obj.has_resolved_marker('mt:apa') )

    def test_add_mantis_id(self):
        obj = logic.Logic()
        self.assertEqual('(mt:a) b', obj.add_mantis_id('a', 'b') )

    def test_teamboxtask_to_mantis_task(self):
        obj = logic.Logic()
        args = { 'id': 123, 'name' : 'apa bepa' }
        self.assertEqual( {'project': '1', 'category': 'teambox_init', 'description': '(teambox 123)', 'summary': 'apa bepa'},  obj.teamboxtask_to_mantis_task(args) )

    def test_remove_mantis_id(self):
        obj = logic.Logic()
        self.assertEqual('apa', obj.remove_mantis_id('apa') )
        self.assertEqual('apa', obj.remove_mantis_id('(mt:1) apa') )
        self.assertEqual('apa', obj.remove_mantis_id('(mt:13) apa') )
        
    def test_extract_hash_from_mantis(self):
        obj = logic.Logic()
        self.assertEqual('a6577e2ab841d66957b0676f7c49b479e23f27e837248649704219e5', obj.extract_hash_from_mantis('(tb:21152349, John Doe - hash:a6577e2ab841d66957b0676f7c49b479e23f27e837248649704219e5)') )
        self.assertEqual('', obj.extract_hash_from_mantis('(tb:21152349, John Doe - a6577e2ab841d66957b0676f7c49b479e23f27e837248649704219e5)') )
        
        
if __name__ == '__main__':
    #ss = unittest.TestSuite()
    #ss.addTest( LogicTest('test_teambox_extract_hash') )
    #unittest.TextTestRunner().run(ss)
    unittest.main()
