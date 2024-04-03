from flask import*
from database import*

user=Blueprint('user',__name__)

@user.route('/userhome',methods=['get','post'])
def userhome():
    return render_template("userhome.html")

@user.route('/sendcomplaints',methods=['get','post'])
def sendcomplaints():
    data={}
    qry="select * from complaints"
    res=select(qry)
    data['u']=res
    print(data['u'])
    if 'complaints' in request.form:
        title=request.form['title']
        des=request.form['description']
        qry="insert into complaints values(null,'%s','%s','%s','pending',curdate())"%(session['uid'],title,des)
        insert(qry)
    return render_template("sendcomplaints.html",data=data)

@user.route('/sendfeedback',methods=['get','post'])
def sendfeedback():
    data={}
    qry="select * from feedback"
    res=select(qry)
    data['u']=res
    print(data['u'])
    if 'feedback' in request.form:
        des=request.form['description']
        qry="insert into feedback values(null,'%s','%s',curdate())"%(session['uid'],des)
        insert(qry)
    return render_template("sendfeedback.html",data=data)

@user.route('/sendreview',methods=['get','post'])
def sendreview():
    data={}
    qry="select * from review"
    res=select(qry)
    data['u']=res
    print(data['u'])
    if 'review' in request.form:
        rev=request.form['review_rating']
        qry="insert into review values(null,'%s','%s',curdate())"%(session['uid'],rev)
        insert(qry)
    return render_template("sendreview.html",data=data)