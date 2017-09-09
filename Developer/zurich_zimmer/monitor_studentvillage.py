from lxml import html
import requests

class Monitoring:
    url = 'http://studentvillage.ch/unterkunfte/'

    def requestPage(url):
        page = requests.get(url)
        tree = html.fromstring(page.content)

        print(tree)
