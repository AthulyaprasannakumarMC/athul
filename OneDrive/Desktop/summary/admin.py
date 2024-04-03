from flask import*
from database import*

admin=Blueprint('admin',__name__)

@admin.route('/adminhome',methods=['get','post'])
def adminhome():
    return render_template("adminhome.html")

@admin.route('/viewuser',methods=['get','post'])
def viewuser():
    data={}
    qry="select * from user"
    res=select(qry)
    data['u']=res
    print(data['u'])
    return render_template("viewuser.html",data=data)

@admin.route('/viewcomplaints',methods=['get','post'])
def viewcomplaints():
    data={}
    qry="select * from complaints inner join user on user.user_id=complaints.sender_id"
    res=select(qry)
    data['u']=res
    print(data['u'])
    return render_template("viewcomplaints.html",data=data)

    
@admin.route('/viewfeedback',methods=['get','post'])
def viewfeedback():
    data={}
    qry="select * from feedback inner join user on user.user_id=feedback.sender_id"
    res=select(qry)
    data['u']=res
    print(data['u'])
    return render_template("viewfeedback.html",data=data)

@admin.route('/sendreply',methods=['get','post'])
def sendreply():
    id=request.args['id']
    data={}
    q="select * from complaints where complaints_id='%s'"%(id)
    res=select(q)
    if res:
        data['view']=res
        print(res,"ppppppppppppppppp")
    if'send'in request.form:
        reply=request.form['reply']
        
        qry="update complaints set reply='%s' where complaints_id='%s'"%(reply,id)
        update(qry)
    
    return render_template("sendreply.html",data=data)

@admin.route('/viewreview',methods=['get','post'])
def viewreview():
    data={}
    qry="select * from review inner join user on user.user_id=review.user_id"
    res=select(qry)
    data['u']=res
    print(data['u'])
    return render_template("viewreview.html",data=data)

