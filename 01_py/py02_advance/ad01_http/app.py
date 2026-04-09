import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

CACHE_CONST_KEY_TYPE = "type"
CACHE_CONST_KEY_FILE_START = "file_start"
CACHE_CONST_KEY_FILE_END = "file_end"

cache_map = {
    'default': {
        CACHE_CONST_KEY_TYPE: 'text',
        CACHE_CONST_KEY_FILE_START: 512,
        CACHE_CONST_KEY_FILE_END: 1024,
    }
}


def get_range_size(range : str) -> (int, int):
    # Range: bytes=256-1024
    range = range.strip()
    range_scope = range.replace("bytes=", "")

    scopes = range_scope.split("-")
    if scopes and len(scopes) == 2:
        return int(scopes[0]), int(scopes[1])
    return 0, 0

def tuple_join(cache_tpl : tuple, req_tpl : tuple):
    """ 取两组范围的交集 """

    cache_tpl1 = cache_tpl[0]
    cache_tpl2 = cache_tpl[1]

    req_tpl1 = req_tpl[0]
    req_tpl2 = req_tpl[1]

    # 范围不存在
    if req_tpl1 == req_tpl2 or cache_tpl1 == cache_tpl2:
        return ()

    if req_tpl1 < cache_tpl1 and req_tpl2 > cache_tpl2:
        return cache_tpl1, cache_tpl2
    if cache_tpl1 < req_tpl1 and cache_tpl2 > req_tpl2:
        return req_tpl1, req_tpl2

    if cache_tpl1 < req_tpl2 < cache_tpl2:
        return cache_tpl1, req_tpl2
    if cache_tpl1 < req_tpl1 < cache_tpl2:
        return req_tpl1, cache_tpl2

    return ()


def tuple_diff(cache_tpl : tuple, req_tpl : tuple):
    """ cache_tpl - req_tpl 缺少哪些数据 """
    # 第一个返回参数表示是否全部命中

    if not cache_tpl:
        return req_tpl

    cache_tpl1 = cache_tpl[0]
    cache_tpl2 = cache_tpl[1]

    req_tpl1 = req_tpl[0]
    req_tpl2 = req_tpl[1]

    # 范围不存在
    if req_tpl1 == req_tpl2 or cache_tpl1 == cache_tpl2:
        return True

    if req_tpl1 < cache_tpl1 and req_tpl2 > cache_tpl2:
        return False, (req_tpl1, cache_tpl1), (cache_tpl2, req_tpl2)

    if cache_tpl1 < req_tpl1 and cache_tpl2 > req_tpl2:
        return True

    if cache_tpl1 < req_tpl2 < cache_tpl2:
        return False, (req_tpl1, cache_tpl1)
    if cache_tpl1 < req_tpl1 < cache_tpl2:
        return False, (cache_tpl2, req_tpl2)

    return False

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        data = None
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
            except Exception:
                data = body
        self._handle(data)

    def do_GET(self):
        self._handle()

    def do_HEAD(self):
        self._error_response(405, "Method Not Allowed")

    def _handle(self, data=None):
        try:
            self._do_handel(data)
        except Exception:
            self.send_error(500)

    def check_cache(self, cache_key) -> (bool, str):
        if cache_key not in cache_map:
            return False, None

        cache_data = cache_map.get(cache_key)

        fstart = cache_data.get(CACHE_CONST_KEY_FILE_START)
        fend = cache_data.get(CACHE_CONST_KEY_FILE_END)
        cache_tpl = (fstart, fend)

        req_range = self._get_request_header("Range")
        if req_range:
            req_range_min, req_range_max = get_range_size(req_range)



        return True, None

    def _get_request_header(self, header: str) -> str:
        return self.headers.get(header, "") or self.headers.get(header.lower(), "")

    def gen_cache_key(self, request_uri):
        return f"ck-{request_uri}"

    def _do_handel(self, data=None):
        # 初始化响应头容器（每个请求必须独立）
        self.response_headers = {}

        cache_key = self.gen_cache_key(self.path)
        # print("uri：", self.path)
        # print("method: ", self.command)
        # print("headers: ", self.headers)
        # print("data: ", data)

        # ...
        # Range: bytes=100-1024
        cache_status, err = self.check_cache(cache_key)
        status = "HIT" if cache_status else "MISS"

        self.set_header("X-Status", status)

        data = {
            "name": "zhangsan"
        }

        self._success_response(data)

    def set_header(self, key, value):
        """设置或覆盖 header"""
        self.response_headers[key] = value

    def remove_header(self, key):
        self.response_headers.pop(key, None)

    def add_header(self, key, value):
        """支持多值 header（如 Set-Cookie）"""
        if key in self.response_headers:
            if isinstance(self.response_headers[key], list):
                self.response_headers[key].append(value)
            else:
                self.response_headers[key] = [self.response_headers[key], value]
        else:
            self.response_headers[key] = value

    def _success_response(self, data):
        self._send_response(200, data, None)

    def _error_response(self, code, message):
        self._send_response(code,None, message)

    def _send_response(self, code, data, message):
        self.send_response(200)
        res = {"code": code}
        if message :
            res["message"] = message
        if data:
            res["data"] = data

        # 编码body
        body = json.dumps(res).encode("utf-8")

        # 发送响应头
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))

        for key, value in self.response_headers.items():
            if isinstance(value, list):
                for v in value:
                    self.send_header(key, v)
            else:
                self.send_header(key, value)

        # 结束响应头
        self.end_headers()

        # 发送响应体
        self.wfile.write(body)


def main():

    server = HTTPServer(('localhost', 8090), MyHTTPRequestHandler)
    print('Started http server on port 8080')
    server.serve_forever()


if __name__ == '__main__':
    main()

# curl -v http://127.0.0.1:8090/test/a.txt
# curl -v http://127.0.0.1:8090/test/a.txt?name=zhangsan
