import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from .view import HTML, CSS, JS


def make_handler(repo):
    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, data, content_type='application/json; charset=utf-8'):
            body = json.dumps(data, ensure_ascii=False).encode() if isinstance(data,(dict,list)) else data
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.end_headers();self.wfile.write(body)

        def read_json(self):
            size=int(self.headers.get('Content-Length','0'))
            if size > 10000: raise ValueError('Requisição muito grande.')
            try: payload=json.loads(self.rfile.read(size))
            except (ValueError,UnicodeDecodeError): raise ValueError('JSON inválido.')
            if not isinstance(payload,dict): raise ValueError('Objeto JSON esperado.')
            return payload

        def task_id(self):
            path=urlparse(self.path).path
            if not path.startswith('/api/tarefas/'):return None
            try:
                val=int(path.rsplit('/',1)[-1]);return val if val > 0 else None
            except ValueError:return None

        def do_GET(self):
            path=urlparse(self.path).path
            if path=='/':return self.respond(200,HTML,'text/html; charset=utf-8')
            if path=='/style.css':return self.respond(200,CSS,'text/css; charset=utf-8')
            if path=='/app.js':return self.respond(200,JS,'text/javascript; charset=utf-8')
            if path=='/api/tarefas':return self.respond(200,repo.list_all())
            task_id=self.task_id()
            if task_id is not None:
                task=repo.get(task_id)
                return self.respond(200,task) if task else self.respond(404,{'erro':'Tarefa não encontrada.'})
            return self.respond(404,{'erro':'Recurso não encontrado.'})

        def do_POST(self):
            if urlparse(self.path).path != '/api/tarefas':return self.respond(404,{'erro':'Recurso não encontrado.'})
            try:
                data=self.read_json(); new_id=repo.add(data.get('titulo',''),data.get('descricao',''))
                return self.respond(201,repo.get(new_id))
            except (ValueError,AttributeError,TypeError) as err:return self.respond(400,{'erro':str(err)})

        def do_PUT(self):
            task_id=self.task_id()
            if task_id is None:return self.respond(404,{'erro':'Recurso não encontrado.'})
            try:
                data=self.read_json()
                found=repo.update(task_id,data.get('titulo',''),data.get('descricao',''),data.get('concluida',False))
                return self.respond(200,repo.get(task_id)) if found else self.respond(404,{'erro':'Tarefa não encontrada.'})
            except (ValueError,AttributeError,TypeError) as err:return self.respond(400,{'erro':str(err)})

        def do_DELETE(self):
            task_id=self.task_id()
            if task_id is None:return self.respond(404,{'erro':'Recurso não encontrado.'})
            return self.respond(200,{'mensagem':'Tarefa excluída.'}) if repo.delete(task_id) else self.respond(404,{'erro':'Tarefa não encontrada.'})
    return Handler
