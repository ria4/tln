"""
This is a mess. Worst: it does not work.
"""

from bs4 import BeautifulSoup
import re

r0 = re.compile(r'^[ ]{2,}', re.MULTILINE)
r1 = re.compile(r'^(\s*)', re.MULTILINE)
r2 = re.compile(r'\s+</(a|span|em|strong)>\s+\.', re.MULTILINE)
r3 = re.compile(r'\s+</(a|span|em|strong)>\s+,', re.MULTILINE)
r4 = re.compile(r'\'\s+<(a|span|em|strong)(.*)(a|span|em|strong)>\s+', re.MULTILINE)
r5 = re.compile(r'\'\s+<(span|em|strong)>(.*)</(span|em|strong)>\s+', re.MULTILINE)

class BeautifulMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 200:
            if response["content-type"].startswith("text/html"):
                response.content = r0.sub('', response.content.decode('utf-8'))
                beauty = BeautifulSoup(response.content)
                response.content = r1.sub(r'\1'*2, beauty.prettify())
                response.content = r2.sub(r'</\1>.', response.content.decode('utf-8'))
                response.content = r3.sub(r'</\1>,', response.content.decode('utf-8'))
                response.content = r4.sub(r'\'<\1\2\3>', response.content.decode('utf-8'))
        return response
