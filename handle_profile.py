# --------------------------
# -------- PROFILES --------
# --------------------------

def getBackgroundColor(user):
    #return 'body{background-color: #4FB0C3;}'
    #5FC0D3
    return primary_color

def getFrameColor(user):
    return light_primary_color

def getCoverColor(user):
    return text_primary_color
    
def getMessageBoxColor(user):
    return text_primary_color

def buildMessage(s,m):
    return '''
          <a href="/user/{0}">{1}</a><br>
          {2}<br><br>'''.format(s,db.user[s]['username'],m)

def getMessages(user):
    return '\n'.join([buildMessage(s,m) for s,m in db.fetchMessages(user)])

def buildUserPage(user):    
    data = {'full_name':db.slug2name(user),
            'slug':user,
            'first_name':db.slug2name(user).split(' ')[0],
            'background_color':getBackgroundColor(user),
            'frame_color':getFrameColor(user),
            'cover_color':getCoverColor(user),
            'message_box_color':getMessageBoxColor(user),
            'messages':Markup(getMessages(user))}
    return render_template('user.html',**data)

@app.route('/user/<user>', methods=['POST','GET'])
def handle_user(user):
    if ip.check(request.remote_addr) == '':
        return redirect('/')

    return buildUserPage(user)
