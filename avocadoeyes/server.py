"""Loopback-only single-session control panel."""
import argparse
import importlib
import json
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .runner import Run

STATIC = Path(__file__).parent / "static"


def make_server(port=7860, run=None):
    session = {"run": run or Run()}
    token = secrets.token_urlsafe(32)
    lock = threading.Lock()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # No request logging of clip names, profile data or credentials.

        def reply(self, status, data, content_type="application/json"):
            payload = json.dumps(data, ensure_ascii=False).encode() if content_type == "application/json" else data
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; img-src 'self' data: blob:; media-src blob:; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(payload)

        def host_ok(self):
            port = self.server.server_address[1]
            return self.headers.get("Host") in (f"127.0.0.1:{port}", f"localhost:{port}")

        def do_GET(self):
            if not self.host_ok():
                return self.reply(403, {"error": "Local Host required"})
            if self.path == "/api/state":
                with lock:
                    return self.reply(200, {**session["run"].snapshot(), "token": token})
            files = {"/": ("index.html", "text/html; charset=utf-8"), "/app.js": ("app.js", "text/javascript"), "/style.css": ("style.css", "text/css")}
            if self.path not in files:
                return self.reply(404, {"error": "Not found"})
            name, mime = files[self.path]
            self.reply(200, (STATIC / name).read_bytes(), mime)

        def do_POST(self):
            origin = self.headers.get("Origin")
            valid_origins = {f"http://127.0.0.1:{self.server.server_address[1]}", f"http://localhost:{self.server.server_address[1]}"}
            if not self.host_ok() or (origin and origin not in valid_origins) or not secrets.compare_digest(self.headers.get("X-Avocado-Token", ""), token):
                return self.reply(403, {"error": "Local session token and origin required"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                limit = 64 * 1024 * 1024 if self.path == "/api/upload" else 2 * 1024 * 1024
                if not 0 < length <= limit:
                    return self.reply(413, {"error": "Request is empty or exceeds size limit"})
                body = self.rfile.read(length)
                if len(body) != length:
                    raise ValueError("Incomplete request")
                with lock:
                    run = session["run"]
                    if self.path == "/api/upload":
                        if self.headers.get("X-Upload-Consent") != "yes":
                            raise ValueError("Confirm permission to process this footage before uploading")
                        run.upload(body, self.headers.get("X-Filename", "clip")[:200])
                    else:
                        data = json.loads(body)
                        if self.path == "/api/config":
                            run.configure(data["config"], data["context"], data["rubric"])
                        elif self.path == "/api/run":
                            run.execute(data.get("step", ""), data.get("mode", "step"))
                        elif self.path == "/api/correct":
                            run.correct(data["step"], data["output"])
                        elif self.path == "/api/reset":
                            session["run"] = Run(adapter=run.adapter)
                        else:
                            return self.reply(404, {"error": "Not found"})
                    return self.reply(200, session["run"].snapshot())
            except Exception as exc:
                self.reply(400, {"error": str(exc)})

    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    return server


def main():
    parser = argparse.ArgumentParser(description="AVocadoEyes local pipeline workbench")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--plugin", action="append", default=[], help="Import your trusted Python module to register new step kinds")
    args = parser.parse_args()
    for module in args.plugin:
        importlib.import_module(module)
    server = make_server(args.port)
    print(f"AVocadoEyes: http://127.0.0.1:{server.server_address[1]} (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
