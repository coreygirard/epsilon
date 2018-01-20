import tarfile
import random
from pprint import pprint
import json

tar = tarfile.open("wikipedia-simple-html.tar")

d = {}
for m in tar.getmembers():
    if '~' in m.name:
        continue
    if not m.name.startswith('simple/articles/'):
        continue

    s = round(m.size/1000)*1000
    d[s] = d.get(s,[])+[m.name]

with open('files_and_lengths.json','w') as f:
    json.dump(d,f,indent=4)
