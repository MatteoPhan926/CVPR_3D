#!/usr/bin/env python3
"""Serve only this probe directory, including its raw and authored artifacts."""
import argparse
import functools
import http.server
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(302)
            self.send_header('Location', '/source/viewer/')
            self.end_headers()
            return
        super().do_GET()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8777)
    parser.add_argument('--bind', default='127.0.0.1')
    args = parser.parse_args()
    server = http.server.ThreadingHTTPServer(
        (args.bind, args.port), functools.partial(Handler, directory=str(ROOT))
    )
    print(f'Car probe viewer: http://{args.bind}:{args.port}/', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
