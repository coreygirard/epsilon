import os
import MySQLdb
import webapp2
import hashlib

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

class DB(object):
    def __init__(self,db):
        self.db = db

    def getUserDataBySlug(self,user):
        user = ''.join([e for e in user if e in list('qwertyuiopasdfghjklzxcvbnm')])

        cursor = self.db.cursor()
        cursor.execute('USE profiles;')
        cursor.execute("SELECT * FROM profiles WHERE id=(SELECT id FROM slug2id WHERE slug='" + user + "');")
        i = cursor.fetchone()

        if i == None:
            return None

        data = {}
        _,data['fullname'],data['firstname'],data['lastname'],data['slug'] = i
        data['profilepicture'] = 'http://little-facebook.appspot.com/static/profile-default-male.png'
        return data

    def hashStr(s):
        return hashlib.md5(s.encode()).hexdigest()
    
    def hashPass(self,e,p):
        return self.hashStr(e+p)

    def validate(self,e,p):
        cursor = self.db.cursor()
        cursor.execute('USE profiles;')
        cursor.execute("SELECT hash FROM email2hash WHERE email='{email}';".format(email=e))
        hashToMatch = cursor.fetchone()[0]
        
        if self.hashPass(e,p) != hashToMatch:
            print('AUTHENTICATION FAILURE: ' + str(self.hashPass(e,p)) + ' != ' + str(hashToMatch))
            return False
            
        cursor.execute("SELECT slug FROM profiles WHERE id=(SELECT id FROM email2id WHERE email='{email}');".format(email=e))
        return cursor.fetchone()[0]


def connect():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return DB(db)



