import re
from collections import Counter

class GenerateUUID(object):
    def __init__(self):
        self.s = {}
        self.n = 0

    def get(self,e):
        assert(type(e) == type('string'))
        if e not in self.s.keys():
            self.s[e] = self.n
            self.n += 1

        return self.s[e]

    def query(self,e):
        print(e)
        assert(type(e) == type('string'))
        if e in self.s.keys():
            return self.s[e]
        else:
            return None

class Page(object):
    def __init__(self,uuid,page):
        self.title = re.sub('_',' ',page['title'].title())
        self.summary = page['summary']

        text = page['text']
        text = text.lower()
        text = re.sub('[.]',' ',text)
        text = re.sub(r'[ ]+',' ',text)
        text = [w for w in text.split(' ') if w != '']

        self.ids = [uuid.get(word) for word in text]

        self.counter = Counter(self.ids)

    def queryId(self,q):
        return self.counter.get(q,0)/sum(self.counter.values())

class DB(object):
    def __init__(self):
        self.uuid = GenerateUUID()
        self.page = {}

    def addPage(self,page):
        data = Page(self.uuid,page)
        self.page[data.title] = data

    def queryWord(self,word):
        i = self.uuid.query(word)
        sites = []
        for k,v in self.page.items():
            score = v.queryId(i)
            if score > 0:
                sites.append((score,k))

        return [s[1] for s in reversed(sorted(sites))]
