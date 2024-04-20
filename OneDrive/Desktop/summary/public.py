from flask import *
from database import *

public=Blueprint('public',__name__)

@public.route('/')
def home():
    
    return render_template('home.html')


@public.route('/login',methods=['GET','POST'])
def login():

    if 'login' in request.form:
        username=request.form['uname']
        password=request.form['pass']
        q="SELECT * FROM login WHERE `username`='%s' AND `password`='%s' "%(username,password)
        res=select(q)
       
        if res:
            session['lid']=res[0]['login_id']
            
            if res[0]['usertype']=="admin":
                return redirect(url_for('admin.admin_home'))
            
            elif res[0]['usertype']=="user":
                q="SELECT * from user WHERE login_id='%s'"%(session['lid'])
                res1=select(q)
                if res1:
            
                    session['uid']=res1[0]['user_id']
                return redirect(url_for('user.user_home'))
            
    return render_template('login.html')


@public.route('/usereg',methods=['get','post'])
def reg():
    
    if 'Register' in request.form:
            
            fname=request.form['fname']
            lname=request.form['lname']
            place=request.form['pla']
            pho=request.form['pho']
            ema=request.form['mail']
            uname=request.form['uname']
            pasw=request.form['pasw']

            q="INSERT INTO login VALUES(NULL,'%s','%s','user')"%(uname,pasw)
            res=insert(q)

            q="INSERT INTO `user` VALUES(NULL,'%s','%s','%s','%s','%s','%s')"%(res,fname,lname,place,pho,ema)
            insert(q)  

            return redirect(url_for('public.login'))

    return render_template('usereg.html')
