"""A plain REST API with one endpoint. No dependencies (standard library only).

Run: python rest_api.py     -> http://127.0.0.1:8001/forecast?city=Kolkata
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

FORECASTS = {"kolkata": 31, "mumbai": 33}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/forecast":
            return self._send(404, {"error": "not found"})
        city = parse_qs(url.query).get("city", [""])[0].lower()
        if city not in FORECASTS:
            return self._send(404, {"error": f"unknown city {city!r}"})
        self._send(200, {"city": city.title(), "temp_c": FORECASTS[city]})

    def _send(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8001), Handler).serve_forever()
