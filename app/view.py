from pathlib import Path
HTML = (Path(__file__).resolve().parent.parent / 'static' / 'index.html').read_bytes()
CSS = (Path(__file__).resolve().parent.parent / 'static' / 'style.css').read_bytes()
JS = (Path(__file__).resolve().parent.parent / 'static' / 'app.js').read_bytes()
