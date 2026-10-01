#!/usr/bin/env python3
"""
run_dashboard.py — redirector al dashboard real.

HISTORIA: antes este script servia dashboard.html (v1) como archivo estatico
en el puerto 9000. Eso quedo obsoleto por dos razones:

  1. El dashboard bueno es dashboard_v2.html, y lo sirve notion_api.py en "/".
  2. dashboard_v2.html hace fetch a rutas relativas ("/api/...").  Servido
     como estatico en el 9000 esas llamadas dan 404: no hay backend ahi.
     Repuntarlo al v2 no alcanzaba; habia que mandarlo al 5000.

Entonces ahora el 9000 simplemente redirige al 5000, para que cualquier
acceso directo o favorito viejo siga funcionando.

Uso real:  python notion_api.py   ->  http://localhost:5000
"""

import http.server
import socketserver

PORT = 9000
DESTINO = "http://localhost:5000"


class Redirector(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header("Location", DESTINO + self.path)
        self.end_headers()

    do_POST = do_GET

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    print()
    print("  Este puerto ya no sirve el dashboard.")
    print(f"  El dashboard real esta en {DESTINO} (lo levanta notion_api.py).")
    print(f"  Redirigiendo todo lo que llegue al {PORT} hacia alla.")
    print()
    print("  Ctrl+C para cerrar.")
    print()
    with socketserver.TCPServer(("", PORT), Redirector) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Cerrado.")
