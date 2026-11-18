"""Testes reais de integração HTTP, executados com servidor local isolado."""
import http.client
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from app.controller import make_handler
from app.model import TaskRepository

class QuietHandler:
    pass

class TestHTTP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.repo=TaskRepository(Path(cls.tmp.name)/'integration.sqlite')
        handler=make_handler(cls.repo)
        handler.log_message=lambda self,*args: None
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join();cls.tmp.cleanup()

    def request(self, method, path, payload=None, raw=None):
        c=http.client.HTTPConnection('127.0.0.1',self.server.server_address[1],timeout=5)
        body=raw if raw is not None else (json.dumps(payload).encode() if payload is not None else None)
        c.request(method,path,body=body,headers={'Content-Type':'application/json'})
        r=c.getresponse();raw_data=r.read();status=r.status;content_type=r.getheader('Content-Type');c.close()
        return status, json.loads(raw_data) if 'application/json' in content_type else raw_data.decode(),content_type

    def create(self,title='Tarefa padrão',desc=''):
        status,data,_=self.request('POST','/api/tarefas',{'titulo':title,'descricao':desc})
        self.assertEqual(status,201)
        return data['id']

    def test_01_home_and_static_assets(self):
        for path,fragment in [('/','Organiza'),('/style.css','body'),('/app.js','fetch')]:
            status,body,_=self.request('GET',path)
            self.assertEqual(status,200);self.assertIn(fragment,body)

    def test_02_create_and_read(self):
        task=self.create('Integração', 'Descrição de teste')
        status,data,_=self.request('GET',f'/api/tarefas/{task}')
        self.assertEqual(status,200);self.assertEqual(data['titulo'],'Integração')

    def test_03_list_tasks(self):
        self.create('Listagem')
        status,data,_=self.request('GET','/api/tarefas')
        self.assertEqual(status,200);self.assertIsInstance(data,list)
        self.assertIn('Listagem',[x['titulo'] for x in data])

    def test_04_update_and_complete(self):
        task=self.create('Antes')
        status,data,_=self.request('PUT',f'/api/tarefas/{task}',{'titulo':'Depois','descricao':'Atualizada','concluida':True})
        self.assertEqual(status,200);self.assertEqual(data['concluida'],1);self.assertEqual(data['titulo'],'Depois')

    def test_05_reopen(self):
        task=self.create('Alternar')
        self.request('PUT',f'/api/tarefas/{task}',{'titulo':'Alternar','concluida':True})
        status,data,_=self.request('PUT',f'/api/tarefas/{task}',{'titulo':'Alternar','concluida':False})
        self.assertEqual(status,200);self.assertEqual(data['concluida'],0)

    def test_06_delete(self):
        task=self.create('Remover')
        status,_,_=self.request('DELETE',f'/api/tarefas/{task}')
        self.assertEqual(status,200)
        self.assertEqual(self.request('GET',f'/api/tarefas/{task}')[0],404)

    def test_07_invalid_empty_title(self):
        s,d,_=self.request('POST','/api/tarefas',{'titulo':'    '})
        self.assertEqual(s,400);self.assertIn('Título',d['erro'])

    def test_08_invalid_long_fields(self):
        for field,value in [('titulo','a'*101),('descricao','a'*501)]:
            data={'titulo':'válida','descricao':''};data[field]=value
            self.assertEqual(self.request('POST','/api/tarefas',data)[0],400)

    def test_09_bad_json(self):
        s,d,_=self.request('POST','/api/tarefas',raw=b'{')
        self.assertEqual(s,400);self.assertIn('JSON',d['erro'])

    def test_10_json_array(self):
        self.assertEqual(self.request('POST','/api/tarefas',raw=b'[]')[0],400)

    def test_11_nonexistent_resource(self):
        for method in ['GET','PUT','DELETE']:
            status,_,_=self.request(method,'/api/tarefas/999999',{'titulo':'n'} if method=='PUT' else None)
            self.assertEqual(status,404)

    def test_12_unknown_routes(self):
        self.assertEqual(self.request('GET','/nao-existe')[0],404)
        self.assertEqual(self.request('POST','/nao-existe',{'titulo':'a'})[0],404)

    def test_13_accents_and_unicode(self):
        task=self.create('Reunião — amanhã','Informações: café ☕')
        s,data,_=self.request('GET',f'/api/tarefas/{task}')
        self.assertEqual(s,200);self.assertEqual(data['descricao'],'Informações: café ☕')

    def test_14_reject_bad_update(self):
        task=self.create('Original')
        status,_,_=self.request('PUT',f'/api/tarefas/{task}',{'titulo':''})
        self.assertEqual(status,400)
        self.assertEqual(self.request('GET',f'/api/tarefas/{task}')[1]['titulo'],'Original')

    def test_15_database_survives_new_repository(self):
        task=self.create('Persistência')
        again=TaskRepository(self.repo.database)
        self.assertEqual(again.get(task)['titulo'],'Persistência')

if __name__=='__main__':unittest.main()
