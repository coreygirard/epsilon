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
        text = page['text']
        text = text.lower()
        text = re.sub('[.]',' ',text)
        text = re.sub(r'[ ]+',' ',text)
        text = [w for w in text.split(' ') if w != '']

        self.ids = [uuid.get(word) for word in text]

        self.counter = Counter(self.ids)

    def queryWord(self,q):
        return self.counter.get(q,0)/sum(self.counter.values())

class DB(object):
    def __init__(self):
        self.uuid = GenerateUUID()
        self.page = {}

    def addPage(self,page):
        title = re.sub('_',' ',page['title'].title())
        data = Page(self.uuid,page)
        self.page[title] = data

    '''
    def parse(self,s):
        s = re.sub(r'[\[].*?[\]]',r'',s)
        s = s.split(' ')
        return Doc([self.uuid.get(e) for e in s])

    def queryWord(self,q):
        results = {}
        for k,v in self.doc.items():
            n = v.counter.get(q,0)
            if n != 0:
                results[k] = n/sum(v.counter.values())

        return results

    def query(self,q):
        q = [self.uuid.query(w) for w in q.split(' ')]

        results = [self.queryWord(w) for w in q]

        s = set(results[0].keys())
        for i in range(1,len(results)):
            s = s & set(results[i].keys())

        score = {e:1.0 for e in s}
        for result in results:
            for k in score.keys():
                score[k] *= result[k]

        return sorted(list(score.items()),key=lambda x : -x[1])[:10]
    '''

