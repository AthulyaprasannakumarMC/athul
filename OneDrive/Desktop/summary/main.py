from flask import*
from database import*
from public import public
from admin import admin
from user import user


# app=Flask(__name__,template_folder='template')

app = Flask(__name__,
            static_url_path='/static/', 
            static_folder='static',
            template_folder='templates')

app.secret_key="bgnfgngf"

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(user)
app.run(debug=True,port=5027,host="0.0.0.0")