from flask import Flask, request, redirect, render_template, Markup, session
from pprint import pprint
import hashlib
import json
import time
import random
import os
import re
import build_results



app = Flask(__name__)

db = build_results.DB()

with open('pages.json','r') as f:
    pages = json.load(f)

#db = build_results.DB()
#for page in pages:
#    db.addPage(page)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    if query == None:
        return redirect('/')

    return repr(db.page.values()[0].ids)

    #results = db.query(query)
    #return repr(results)


    #query = query.split(' ')
    #return repr(query)
    #return '\n'.join(['query:'+str(query)]+[re.sub('_',' ',result.title()) for result,score in db.query(query)])

if __name__ == '__main__':
    app.run(debug=True)
