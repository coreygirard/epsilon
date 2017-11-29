from flask import Flask, request, redirect, render_template, Markup
import pickle
from pprint import pprint
import hashlib
import json
import time
import random
import MySQLdb
import os

#import handle_login as login
#import handle_db


app = Flask(__name__)

'''
dark_primary_color    = '#1976D2'
primary_color         = '#2196F3'
light_primary_color   = '#BBDEFB'
text_primary_color    = '#FFFFFF'
accent_color          = '#03A9F4'
primary_text_color    = '#212121'
secondary_text_color  = '#757575'
divider_color         = '#BDBDBD'
'''
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

cloudsql_unix_socket = os.path.join('/cloudsql', CLOUDSQL_CONNECTION_NAME)
db = MySQLdb.connect(unix_socket=cloudsql_unix_socket,user=CLOUDSQL_USER,passwd=CLOUDSQL_PASSWORD)


'''

def hashStr(s):
    return hashlib.md5(s.encode()).hexdigest()

class DB(object):
    def __init__(self):
        self.user = {}
        self.slug = {}
    
    def read(self,filename):
        try:
            with open(filename,'r') as dbFile:
                self.user = json.load(dbFile)
        except:
            self.user = {}

    def write(self,filename):
        with open(filename,'w') as dbFile:
            json.dump(db,dbFile,indent=4)
    
    def checkExists(self,email):
        if email in self.slug:
            if self.slug[email] in self.user:
                return True

        return False
            
    def email2slug(self,email):
        return self.slug[email]
        
    def slug2name(self,s):
        return self.user[s]['username']
        
    def addMessage(self,fr,to,message):
        self.user[to]['messages'].insert(0,(fr,message))
        
    def fetchMessages(self,s):
        return self.user[s]['messages']
        
    def addUser(self,email,username,password):
        s = ''.join([e for e in (username.lower()).split(' ')])
        self.user[s] = {'email':email,'username':username,'slug':s,'password':hashStr(email+password),'messages':[]}
        self.slug[email] = s
        return (0,s)
    
    def validateRegister(self,email,username,password):
        if db.checkExists(email):
            return (-1,'Account exists for "' + email + '"')
        
        return self.addUser(email,username,password)

    def validateLogin(self,email,password):
        if not db.checkExists(email):
            return (-1,'Account not found')
        
        slug = self.email2slug(email)
        if self.user[slug]['password'] == hashStr(email+password):
            return (0,slug)
        else:
            return (-1,'Incorrect password')


db = DB()

db.addUser('aim.to.misbehave@bluesun.net','Malcolm Reynolds','captain')
db.addUser('place@holder.com','Zoe Washburne','???')
db.addUser('inevitablebetrayal@bluesun.net','Hoban Washburne','leaf')
db.addUser('deepspace@hotmail.net','Inara Serra','hohoho')
db.addUser('vera@bluesun.net','Jayne Cobb','chainofcommand')
db.addUser('fancygirl@bluesun.net','Kaylee Frye','shinyshinyshiny')
db.addUser('s.tam@osiris.edu','Simon Tam','dropout4lyfe')
db.addUser('brosbeforehos@bluesun.net','River Tam','psychicninja')
db.addUser('godshomie@bluesun.net','Derrial Book','closetatheist')

db.addMessage('inaraserra','malcolmreynolds','Come help me!')

class IP(object):
    def __init__(self):
        self.active = {}
        self.duration = 60*60 # one hour
        self.extend = True

    def enroll(self,i,slug):
        self.active[i] = {'slug':slug,
                          'expires':int(time.time()) + self.duration}

    def renew(self,i):
        if i in self.active:
            self.active[i]['expires'] = int(time.time()) + self.duration

    def check(self,i):
        t = int(time.time())
        self.active = {k:v for k,v in self.active.items() if v['expires'] > t}
        if i in self.active:
            self.renew(i)
            return self.active[i]['slug']
        else:
            return ''

    def purge(self,s):
        if s in self.active:
            del self.active[s]


ip = IP()

#ip.enroll('127.1.1.1','c@girard.com')
#ip.enroll('127.2.2.2','a@geary.com')
#ip.enroll('127.0.0.1','kayleefrye')

@app.route('/', methods=['POST','GET'])
def handle_home():
    s = ip.check(request.remote_addr)
    if s == '':
        return redirect('/login')
    else:
        return redirect('/user/'+s)

# -------------------------
# -------- POSTING --------
# -------------------------

@app.route('/post/<user>', methods=['POST','GET'])
def handle_post(user):
    r = ip.check(request.remote_addr)
    if r == '':
        return redirect('/login')
    else:
        db.addMessage(r,user,request.args.get('message'))
        return redirect('/user/'+user)
'''



    





#@app.route('register')
#def handle_register():
#    return redirect('/login#register')



#@app.route('/')
#def index():
#    pass

#app.add_url_rule('/','index',index)

'''
db = {'johnsmith':{'fullname':'John Smith',
                   'firstname':'John',
                   'lastname':'Smith',
                   'slug':'johnsmith',
                   'personalurlfull':'http://www.johnsmith.com',
                   'personalurlpretty':'johnsmith.com',
                   'profilepicture':'http://little-facebook.appspot.com/static/profile-default-male.png'},
      'coreygirard':{'fullname':'Corey Girard',
                     'firstname':'Corey',
                     'lastname':'Girard',
                     'slug':'coreygirard',
                     'personalurlfull':'http://www.coreygirard.com',
                     'personalurlpretty':'coreygirard.com',
                     'profilepicture':'http://little-facebook.appspot.com/static/profile-default-male.png'}}
'''


@app.route('/search')
def handle_search():
    return 'You searched for: ' + request.args.get('q')

@app.route('/me', methods=['POST','GET'])
def handle_me():
    return redirect('user/coreygirard')

@app.route('/user/<user>', methods=['POST','GET'])
def handle_profile(user):
    user = ''.join([e for e in user if e in list('qwertyuiopasdfghjklzxcvbnm')])
    
    cursor = db.cursor()
    cursor.execute('USE profiles;')
    cursor.execute("SELECT * FROM profiles WHERE id=(SELECT id FROM slug2id WHERE slug='" + user + "');")
    i = cursor.fetchone()
    
    if i == None:
        return 'USER NOT FOUND'

    data = {}
    _,data['fullname'],data['firstname'],data['lastname'],data['slug'] = i
    data['profilepicture'] = 'http://little-facebook.appspot.com/static/profile-default-male.png'
    data['css_loc'] = 'http://little-facebook.appspot.com/static/styles.css'
    
    return render_template('bookFACE_profile.html',**data)

@app.route('/login')
def handle_login():
    data = {'css_loc':'http://little-facebook.appspot.com/static/styles.css'}
    return render_template('bookFACE_login.html',**data)


if __name__ == '__main__':
    app.run(debug=True)
