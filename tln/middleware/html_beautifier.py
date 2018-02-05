from bs4 import BeautifulSoup

class BeautifulMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 200:
            if response["content-type"].startswith("text/html"):
                beauty = BeautifulSoup(response.content)
                response.content = beauty.prettify()
        return response