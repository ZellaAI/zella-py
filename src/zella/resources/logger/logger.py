class Logger:
    def __init__(self, client):
        self.client = client
        pass

    def log(self, action, request, response, user=None, meta=None):
        log_request = {
            "action": action,
            "request": request,
            "response": response
        }
        if user:
            log_request["user"] = user
        if meta:
            log_request["meta"] = meta
        
        data = self.client.post(self.client.base_url + "/log", log_request)
        return data