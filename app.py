from flask import Flask, request
from urllib.parse import quote
from scraping import Scraping

app = Flask(__name__)

def process(str):
    return quote(str)

@app.route("/")
def main():
    web = request.args.get("web")
    title = request.args.get("title")
    page = request.args.get("page")

    if(web and title):
        if(web == 'libgen'):
            url = "https://libgen.is/search.php?req=" + process(title) + "&open=0&res=25&view=simple&phrase=1&column=title"
            scr = Scraping(url)
            list_scrap = scr.libgen()
            return list_scrap
        else:
            return title
    else:
        return "Welcome"