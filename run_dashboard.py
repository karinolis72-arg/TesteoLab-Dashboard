#\!/usr/bin/env python3
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 9000
DIRECTORY = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/dashboard.html'
        return super().do_GET()

os.chdir(DIRECTORY)

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"\n✅ TesteoLab Dashboard iniciado")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"📱 Móvil (mismo WiFi): http://[TU_IP]:{PORT}")
    print(f"\n🧭 NAUTA esperando a las 21:00...")
    print(f"\nPresiona CTRL+C para cerrar el servidor\n")
    
    # Abrir navegador automáticamente (opcional)
    try:
        webbrowser.open(f"http://localhost:{PORT}", new=2)
    except:
        pass
    
    httpd.serve_forever()
