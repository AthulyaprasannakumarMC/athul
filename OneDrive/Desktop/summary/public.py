from flask import*
from database import*


public=Blueprint('public',__name__)


@public.route('/')
def home():
    return render_template("home.html")


@public.route('/login',methods=['get','post'])
def login():
    if'login' in request.form:
        uname=request.form['uname']
        passw=request.form['password']
        qry="select * from login where username='%s' and password='%s'"%(uname,passw)
        res=select(qry)
        if res:
            session['lid']=res[0]['login_id']
            if res:
                utype=res[0]['usertype']
                
                if utype=='admin':
                    return redirect(url_for('admin.adminhome'))
                elif utype=='user':
                    a="select * from user where login_id='%s'"%(session['lid'])
                    q=select(a)
                    session['uid']=q[0]['user_id']
                    return redirect(url_for('user.userhome'))
            
                
    return render_template("login.html")

@public.route('/register',methods=['get','post'])
def register():
    if'register'in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        address=request.form['address']
        phone=request.form['phone']
        place=request.form['place']
        username=request.form['username']
        password=request.form['password']
        
        a="insert into login values(null,'%s','%s','user')"%(username,password)
        res=insert(a)
        
        qry1="insert into user values(null,'%s','%s','%s','%s','%s','%s')"%(res,fname,lname,address,phone,place)
        insert(qry1)
        
        
        
    
    return render_template("registration.html")


