from http.server import ThreadingHTTPServer
import os
from app.model import TaskRepository
from app.controller import make_handler

if __name__ == '__main__':
    port=int(os.getenv('PORT', '8000'))
    repository=TaskRepository(os.getenv('DB_PATH', 'tarefas.db'))
    server=ThreadingHTTPServer(('127.0.0.1',port),make_handler(repository))
    print(f'Abra http://127.0.0.1:{port} no navegador (Ctrl+C para encerrar).')
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
