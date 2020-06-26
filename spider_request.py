from requests import Request

class ClassRequest(Request):
    def __init__(
            self,
            url,
            domain,
            callback=None,
            method='GET',
            data=None,
            headers=None,
            timeout=20
        ):
        Request.__init__(self, method, url, headers, data)
        self.callback = callback
        self.domain = domain
        self.timeout = timeout


