import tempfile,unittest
from pathlib import Path
from app.model import TaskRepository

class TestTasks(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.repo=TaskRepository(Path(self.temp.name)/'db.sqlite3')
    def tearDown(self):self.temp.cleanup()
    def test_create_and_list(self):
        tid=self.repo.add('Estudar','Capítulo 1')
        self.assertEqual(self.repo.get(tid)['titulo'],'Estudar')
        self.assertEqual(len(self.repo.list_all()),1)
    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):self.repo.add('    ')
    def test_long_title_rejected(self):
        with self.assertRaises(ValueError):self.repo.add('a'*101)
    def test_long_description_rejected(self):
        with self.assertRaises(ValueError):self.repo.add('Boa','a'*501)
    def test_update_and_complete(self):
        tid=self.repo.add('Inicial')
        self.assertTrue(self.repo.update(tid,'Final','desc',True))
        self.assertEqual(self.repo.get(tid)['concluida'],1)
    def test_delete(self):
        tid=self.repo.add('Excluir')
        self.assertTrue(self.repo.delete(tid))
        self.assertIsNone(self.repo.get(tid))
    def test_missing_item(self):
        self.assertFalse(self.repo.update(999,'Não existe'))
        self.assertFalse(self.repo.delete(999))
if __name__=='__main__':unittest.main()
