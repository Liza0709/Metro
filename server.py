import http.server
import socketserver
import urllib.parse
import json
import psycopg2

DB_CONFIG = {
    "dbname": "metro_msk",
    "user": "postgres", 
    "password": "BaSik239971177",
    "host": "127.0.0.1",
    "port": "5432"
}
class MetroHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == '/api/stations-list':
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM stations ORDER BY name")
            stations = [{'id': r[0], 'name': r[1]} for r in cur.fetchall()]
            cur.close()
            conn.close()
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(stations, ensure_ascii=False).encode())
        elif path.startswith('/station/'):
            station_id = path.split('/')[-1]
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            cur.execute("SELECT name FROM stations WHERE id = %s", (station_id,))
            station = cur.fetchone()
            if not station:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Station not found')
                return
            
            cur.execute("SELECT name FROM landmarks WHERE station_id = %s ORDER BY name", (station_id,))
            landmarks = [r[0] for r in cur.fetchall()]
            cur.close()
            conn.close()
            
            items = ''.join(f'<li>№ {l}</li>' for l in landmarks) or '<li>ааЕб аДаОббаОаПбаИаМаЕбаАбаЕаЛбаНаОббаЕаЙ</li>'

            html = f"""<!DOCTYPE html>

<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>{station[0]} - аДаОббаОаПбаИаМаЕбаАбаЕаЛбаНаОббаИ</title>
    <link rel="stylesheet" href="/css/style.css">
</head>

<body>
    <div class="container">
        <a href="/" class="back-button">т ааАаЗаАаД аК ббаЕаМаЕ</a>
        <h1 class="station-title">№ {station[0]}</h1>
        <ul class="landmarks-list">
            {items}
        </ul>
    </div>
</body>
</html>"""
          
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode())

        elif path.startswith('/js/'):
            with open('frontend' + path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.end_headers()
                self.wfile.write(f.read())
        elif path.startswith('/css/'):
            with open('frontend' + path, 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(f.read())

        elif path == '/':
            with open('frontend/index.html', 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404')

if __name__ == '__main__':
    with socketserver.TCPServer(("127.0.0.1", 8000), MetroHandler) as httpd:
        print('аЁаЕбаВаЕб аЗаАаПббаЕаН аНаА http://127.0.0.1:8000')
        print('Ctrl+C аОббаАаНаОаВаКаА')
        httpd.serve_forever()