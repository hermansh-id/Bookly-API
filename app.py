from flask import Flask, request
from urllib.parse import quote
from flask_cors import CORS, cross_origin
from scraping import Scraping

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def process(str):
    return quote(str)

@app.route("/")
@cross_origin()
def main():
    web = request.args.get("web")
    title = request.args.get("title")
    start = request.args.get('start', 1, type=int)
    length = request.args.get('length', 5, type=int)
    draw = request.args.get('draw', type=int)
    
    if(web and title):
        if(web == 'libgen'):
            url = "https://libgen.is/search.php?req=" + process(title) + "&open=0&res=25&view=simple&phrase=1&column=title"
            scr = Scraping(url=url, start=start, per_page=length, draw=draw)
            list_scrap = scr.libgen()
            return list_scrap
        else:
            return title
    else:
        return "Welcome"