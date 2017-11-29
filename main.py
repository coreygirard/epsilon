from flask import Flask, request, redirect, render_template, Markup, session
from pprint import pprint
import hashlib
import json
import time
import random
import os
import re


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
        assert(type(e) == type('string'))
        if e in self.s.keys():
            return self.s[e]
        else:
            return None

class Doc(object):
    def __init__(self,ids):
        self.ids = ids
        self.counter = {}
        for i in ids:
            self.counter[i] = self.counter.get(i,0)+1

class DB(object):
    def __init__(self):
        self.uuid = GenerateUUID()
        self.doc = {}

    def parse(self,s):
        s = re.sub(r'[\[].*?[\]]',r'',s)
        s = s.split(' ')
        return Doc([self.uuid.get(e) for e in s])

    def addDoc(self,k,v):
        self.doc[k] = self.parse(v)

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

db = DB()

with open('raw.json','r') as f:
    raw = json.load(f)

for k,v in raw.items():
    db.addDoc(k,v)



app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('q')

    return '\n'.join([re.sub('_',' ',result.title()) for result,score in db.query(query)])

if __name__ == '__main__':
    app.run(debug=True)
