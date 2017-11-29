# -----------------------
# -------- LOGIN --------
# -----------------------

def validateLogin(args):
    if args.get('email','') == '':
        return (-1,'"Email" is a required field')
    else:
        email = args['email']

    if args.get('password','') == '':
        return (-1,'"Password" is a required field')
    else:
        password = args['password']

    return db.validateLogin(email,password)    

def getLoginPage(response):
    data = {'background_color':'body{background-color:' + primary_color + ';}',
            'frame_color':light_primary_color,
            'cover_color':text_primary_color,
            'response':response,
            'css_loc':'static/styles.css'}
    
    return render_template('bookFACE_login.html',**data)

    return page

@app.route('/handle/login', methods=['POST','GET'])
def handle__login():
    return render_template('bookFACE_profile.html',**{'css_loc':'static/styles.css'})
    
@app.route('/handle/register', methods=['POST','GET'])
def handle__register():
    return render_template('bookFACE_profile.html',**{'css_loc':'static/styles.css'})
    
@app.route('/login', methods=['POST','GET'])
def handle_login():
    if 'email' not in request.args:
        return getLoginPage('')
    
    response = validateLogin(request.args)
    if response[0] != 0:
        return getLoginPage(response[1])
    else:
        ip.enroll(request.remote_addr,response[1])
        return redirect('/')


# -----------------------
# -------- LOGOUT --------
# -----------------------

def handle_logout():
    ip.purge(request.remote_addr)
    return redirect('/')

# ------------------------------
# -------- REGISTRATION --------
# ------------------------------

def validateRegister(args):
    if args.get('email','') == '':
        return (-1,'"Email" is a required field')
    else:
        email = args['email']
    
    if args.get('username','') == '':
        return (-1,'"Username" is a required field')
    else:
        username = args['username']

    if args.get('password','') == '':
        return (-1,'"Password" is a required field')
    else:
        password = args['password']
        
    if '@' not in email or '.' not in email:
        return (-1,"Invalid email address")

    if password == 'p@$$w0rd':
        return (-1,'Seriously?')
        
    return db.validateRegister(email,username,password)


def getRegisterPage(response):
    data = {'background_color':'body{background-color:' + primary_color + ';}',
            'frame_color':light_primary_color,
            'cover_color':text_primary_color,
            'response':response,
            'css_loc':'static/styles.css'}
    
    return render_template('bookFACE_register.html',**data)

def register():
    if 'email' not in request.args:
        return getRegisterPage('')
    
    response = validateRegister(request.args)
    if response[0] == -1:
        return getRegisterPage(response[1])
    else:
        #db.write('db.json')

        ip.enroll(request.remote_addr,response[1])
        return redirect('/')


