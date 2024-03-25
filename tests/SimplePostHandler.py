from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

def get_test_response():
    return '{"id": "completion-unique-id","object": "text_completion","created": 1589478378,"model": "text-davinci-003","choices": [    {    "text": "This is the generated text from the model based on your prompt.",    "index": 0,    "logprobs": null,    "finish_reason": "length"    }],"usage": {    "prompt_tokens": 10,    "completion_tokens": 15,    "total_tokens": 25}}'

class SimplePostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode("utf-8")

        print(f"Serving request {post_data}")

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()

        response = get_test_response()
        self.wfile.write(response.encode('utf-8'))

if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimplePostHandler)
    httpd.serve_forever()