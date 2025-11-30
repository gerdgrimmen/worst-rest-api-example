# https://github.com/ynsrc/python-simple-rest-api/blob/main/server.py
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 5005
api_data = {
    "data": {}
}
class API():
    def __init__(self):
        self.routing = { "GET": { }, "POST": { } , "PUT": { } , "DELETE": { } }
    
    def get(self, path):
        def wrapper(fn):
            self.routing["GET"][path] = fn
        return wrapper

    def post(self, path):
        def wrapper(fn):
            self.routing["POST"][path] = fn
        return wrapper

    def put(self, path):
        def wrapper(fn):
            self.routing["PUT"][path] = fn
        return wrapper

    def delete(self, path):
        def wrapper(fn):
            self.routing["DELETE"][path] = fn
        return wrapper

api = API()

@api.get("/")
def index(_):
    return { 
        "name": "Minimal Rest API example",
        "summary": "",
        "endpoints": [ "/data", "imagedata", "/help" ],
        "version": "0.2.0"
    }

@api.get("/help")
def get_help(args):
    return {"help": "help"}

@api.get("/data")
def get_data(args):
    if "path_id" in args.keys():
        if args["path_id"] in api_data["data"].keys():
            return api_data["data"][args["path_id"]]
        else:
            return {"message": "not found"}
    return {"data": api_data["data"]}

@api.get("/data/<id>")
def get_signle_data(args, id):
    if "path_id" in args.keys():
        if args["path_id"] in api_data["data"].keys():
            return api_data["data"][args["path_id"]]
        else:
            return {"message": "not found"}
    return {"data": api_data["data"]}

@api.post("/data")
def post_data(body):
    if not "text" in body.keys():
        return {"message": "invalid entry"}
    next_id = len(api_data["data"].keys())
    api_data["data"][next_id] = body["text"]
    return {"id": str(next_id)}

@api.put("/imagedata")
def post_image(body):
    next_id = len(api_data["data"].keys())
    api_data["data"][next_id] = body
    return {"id": str(next_id)}

@api.delete("/data")
def delete_data(body):
    if not "id" in body.keys():
        return {"message": "invalid am entry"}
    print(body)
    print(api_data["data"].keys())
    if int(body["id"]) in api_data["data"].keys():
        api_data["data"].pop(int(body["id"]))
        print("deleting")
        return {"message": "deleted"}
    return {"message": "not found"}

if __name__ == "__main__":
    class ApiRequestHandler(BaseHTTPRequestHandler):
        global api
        
        def call_api(self, method, path, args):
            if path in api.routing[method]:
                try:
                    result = api.routing[method][path](args)
                    self.send_response(200)
                    self.end_headers()
                    if type(result) is dict:
                        self.wfile.write(json.dumps(result, indent=4).encode())
                    elif type(result) is str:
                        self.wfile.write(result.encode())
                    elif type(result) is bytes:
                        self.wfile.write(result.encode())
                except Exception as e:
                    self.send_response(500, "Server Error")
                    self.end_headers()
                    self.wfile.write(json.dumps({ "error": e.args }, indent=4).encode())
            else:
                self.send_response(404, "Not Found")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "not found"}, indent=4).encode())

        def return_404(self):
            self.send_response(404, "Not Found")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}, indent=4).encode())
        
        def return_401(self):
            self.send_response(401, "Not Authorized")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "not found"}, indent=4).encode())
        
        def return_400(self):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "posted data must be in json format"}, indent=4).encode())

        def do_GET(self):
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            args = parse_qs(parsed_url.query)
            if path in api.routing["GET"]: 
                self.call_api("GET", path, args)
                return
            else:
                new_path, path_id = path.rsplit("/",1)
                if new_path+"/<id>" in api.routing["GET"]:
                    args["/<id>"] = path_id
                    self.call_api("GET", new_path+"/<id>", args, path_id)
                    return
            self.return_404()


        def do_POST(self):
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            if self.headers.get("content-type") != "application/json":
                self.return_400()
                return
            else:
                data_len = int(self.headers.get("content-length"))
                data = self.rfile.read(data_len).decode()
                if path in api.routing["POST"]:
                    self.call_api("POST", path, json.loads(data))
                    return
            self.return_404()

        def do_PUT(self):
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            if self.headers.get("content-type") != "image/png":
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "posted data must be in an png image format"
                }, indent=4).encode())
            else:
                data_len = int(self.headers.get("content-length"))
                data = self.rfile.read(data_len)
                self.call_api("PUT", path, data)

        def do_DELETE(self):
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            if self.headers.get("content-type") != "application/json":
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "posted data must be in json format"
                }, indent=4).encode())
            else:
                data_len = int(self.headers.get("content-length"))
                data = self.rfile.read(data_len).decode()
                self.call_api("DELETE", path, json.loads(data))

    httpd = HTTPServer(('', PORT), ApiRequestHandler)
    print(f"Application started at http://127.0.0.1:{PORT}/")
    httpd.serve_forever()