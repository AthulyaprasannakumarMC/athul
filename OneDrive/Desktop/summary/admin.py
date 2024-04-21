from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adhome')
def admin_home():
    return render_template('admnhome.html')

@admin.route("/admviewuser",methods=['get','post'])
def viewuser():
		data={}
		q="select * from user"
		data['view']=select(q)
		return render_template("admviewuser.html",data=data)

@admin.route("/admviewcomp",methods=['get','post'])
def viewcomp(): 
		data={}
		q="SELECT * from complaints inner join user using(user_id)"
		data['comp']=select(q)
		return render_template("viewcomp.html",data=data)

# @admin.route("/admwordtodesc",methods=['get','post'])
# def viewdesc(): 
# 		data={}
# 		q="SELECT * from word inner join user using(user_id)"
# 		data['wrd']=select(q)
# 		return render_template("admvieword.html",data=data)

@admin.route("/admin_sendreply", methods=['get', 'post'])
def adm_serep():
            data = {}   
            compid=request.args['id']
            usid=request.args['userid']
            if 'send' in request.form:
                reply = request.form['rep']
                q = "UPDATE `complaints` SET `reply`='%s' WHERE `complaint_id`='%s'"%(reply,compid)
                insert(q)
                q="SELECT * FROM `complaints` WHERE `user_id`='%s'"%(usid)	
                data['view']=select(q)
                return redirect(url_for('admin.viewcomp'))
            return render_template('sendrep.html',data=data)


@admin.route("/admviewfbck",methods=['get','post'])
def viewfb(): 
		data={}
		q="SELECT * from feedback inner join user using(user_id)"
		data['fbc']=select(q)
		return render_template("viewfeedback.html",data=data)


@admin.route("/admviewfiles",methods=['get','post'])
def viewfil():   
		data={}
		q="SELECT * from files inner join user using(user_id)"
		data['fbc']=select(q)
		return render_template("admnviewfiles.html",data=data)


@admin.route("/sumres", methods=['get', 'post'])
def viewres():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM general_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("admnviewsummary.html", data=data)

import pyttsx3

@admin.route("/text_to_audio", methods=['GET'])
def text_to_audio():
    text = request.args.get('text')
    print(text,'+++++++++++++++++++++=')

    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Set properties for the TTS engine
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)   # Volume (0.0 to 1.0)

    # Convert the text to speech
    engine.say(text)

    # Play the speech
    engine.runAndWait()

    return "Audio played successfully"

@admin.route("/highres", methods=['get', 'post'])
def viewhighrankres():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM high_rank_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("admnviewhighrank.html", data=data)

@admin.route("/keyres", methods=['get', 'post'])
def keyres():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM keywords_summary inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("admnviewkeywdsum.html", data=data)

@admin.route("/simpleres", methods=['get', 'post'])
def simpleres():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM simple_words_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("admnviewsimwds.html", data=data)


@admin.route("/gptres", methods=['get', 'post'])
def ideares():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM gpt_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("admnviewgptsum.html", data=data)


@admin.route("/sentres", methods=['get', 'post'])
def sentires():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM sentiment_analysis_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("admnviewsenti.html", data=data)


@admin.route("/translate", methods=['GET'])
def translate():
    summary = request.args.get('text')
    return render_template("translate.html",summary=summary)


from googletrans import Translator 

@admin.route("/translate_summary", methods=["POST"])
def translate_summary():
    print('***********')
    data = request.json
    print(data,'///////////')
    summary = data.get('summary')
    print('00000')
    target_language = data.get("target_language", "en")
    print(target_language)

    # Ensure summary is not None before proceeding
    if summary is None:
        return jsonify({"error": "Summary is missing in the request."}), 400

    translated_summary = ""
    try:
        translator = Translator()
        translated_summary = translator.translate(summary, dest=target_language).text
        print("translated_summary: ", translated_summary)
    except Exception as e:
        print("Error translating summary:", e)
        return jsonify({"error": "Failed to translate summary."}), 500

    return jsonify({"translated_summary": translated_summary})
