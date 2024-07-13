import http.server
import socketserver
import logging
import os

PORT = 8000
DIRECTORY = "web"

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        logging.info("%s - - [%s] %s\n" %
                     (self.client_address[0],
                      self.log_date_time_string(),
                      format % args))
    
    def translate_path(self, path):
        # Serve files from the specified directory
        path = http.server.SimpleHTTPRequestHandler.translate_path(self, path)
        return os.path.join(DIRECTORY, os.path.relpath(path, os.getcwd()))

    def send_error(self, code, message=None):
        if code == 404:
            self.path = "/404.html"
            return self.do_GET()
        return super().send_error(code, message)

if __name__ == "__main__":
    logging.basicConfig(filename='server.log', level=logging.INFO)
    os.chdir(DIRECTORY)
    
    handler = RequestHandler
    httpd = socketserver.TCPServer(("", PORT), handler)

    print(f"Serving HTTP on port {PORT}")
    httpd.serve_forever()