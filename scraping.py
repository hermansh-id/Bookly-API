import requests
from bs4 import BeautifulSoup

class Scraping:
    
    def __init__(self, url, start, per_page, draw):
        self.url = url
        self.start = start
        self.per_page = per_page
        self.draw = draw
    
    def get_page(self):
        page = requests.get(self.url)
        return page.content

    def parsing(self):
        page = self.get_page()
        soup = BeautifulSoup(page, "html.parser")
        return soup
    
    def get_last(self):
        parse = self.parsing()
        table = parse.find_all("table")[3]
        if(table.text == '') : return [False, '']
        next = len(table.find_all("td")[1].find_all("a")) == 2 or table.find("a").text.strip() == "►"
        if(next):
            if(len(table.find_all("td")[1].find_all("a")) == 2):
                link = table.find_all("a")[1]['href'] 
            else:
                link = table.find_all("a")[0]['href']
        else:
            link = ""
        return [next, link]
        
        
    def scraping_libgen(self):
        parse = self.parsing()
        rows = list()
        table = parse.find_all("table")[2]
        tr = table.find_all("tr")[1:]
        for t in tr:
            td = t.find_all("td")
            row = {
                "id": td[0].text,
                "author": td[1].text,
                "title": td[2].text,
                "publisher": td[3].text,
                "extension": td[8].text,
                "link": [td[9].find("a")["href"], td[10].find("a")["href"]]
            }
            rows.append(row)
        return rows
    
    def paginate(self, rows):
        start = (self.per_page * self.start)
        if((len(rows) >= start + 1 + self.per_page) and (self.per_page != -1)):
            return rows[start:start + self.per_page]
        elif((len(rows) >= start + 1 + self.per_page) and (self.per_page == -1)):
            return rows[start:len(rows)]
        else:
            return rows
    
    def libgen(self):
        rows = []
        row = self.scraping_libgen()
        rows = rows + row
        next = self.get_last()
        
        while(next[0]):
            self.url = "https://libgen.is/"+next[1]
            row = self.scraping_libgen()
            rows + row
            next = self.get_last()
        
        # filteredData = self.paginate(rows)
        data = {
            'data': rows,
            'recordsFiltered': len(rows),
            'recordsTotal': len(rows),
            'draw': self.draw
        }
        return data
        
