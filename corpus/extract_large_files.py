import tarfile
import random
from pprint import pprint
import json

tar = tarfile.open("wikipedia-simple-html.tar")


with open('files_and_lengths.json','r') as f:
    files = json.load(f)

files_list = list(reversed(sorted([(int(k),len(v)) for k,v in files.items()])))

target = sum([e[1] for e in files_list]) * 0.25

keep = []
n = 0
while n < target:
    temp = files_list.pop(0)
    n += temp[1]
    keep.append(temp)

keep_files = []
for k,_ in keep:
    keep_files += files[str(k)]

for m in tar.getmembers():
    if m.name in keep_files:
        tar.extract(m.name)


'''
for m in tar.getmembers():
    if '~' in m.name:
        continue
    if not m.name.startswith('simple/articles/'):
        continue

    s = round(m.size/1000)*1000

    d[s] = d.get(s,[])+[m.name]
'''
