from typing import Counter
import uuid
from flask import *
from database import *

user=Blueprint('user',__name__)

@user.route('/ushome')
def user_home():
    return render_template('userhome.html')


@user.route("/usersendcomp", methods=['get', 'post'])   
def secomp():
    if not session.get("lid") is None:
         data = {}
         if 'Add' in request.form:
                complaint = request.form['comp']
                q = "INSERT INTO `complaints`(`complaint_id`,`user_id`,`complaint`,`reply`,`date`) VALUES(NULL,'%s','%s','%s',now())" % (session['uid'], complaint, 'Pending')
                insert(q)
                return redirect(url_for('user.secomp'))
    q="select * from complaints where user_id='%s'"%(session['uid'])
    data['vie']=select(q)   
    return render_template('user_send_comp.html',data=data)


@user.route("/user_viewrep", methods=['get', 'post'])
def user_view_reply():
    if not session.get("lid") is None:
        data = {}
        coid=request.args['compl_id']
        qr = "SELECT * FROM complaints WHERE complaint_id='%s'"%(coid)
        data['view'] = select(qr)

    return render_template("userviewreplies.html", data=data)


@user.route("/fdbck", methods=['get', 'post'])
def sendfb():
    if not session.get("lid") is None:
         data = {}
         if 'Add' in request.form:
                f = request.form['fbck']
                q = "INSERT INTO `feedback`(`feedback_id`,`user_id`,`description`,`date`) VALUES(NULL,'%s','%s',now())" % (session['uid'], f)
                insert(q)
                return redirect(url_for('user.sendfb'))  
    q="select * from feedback where user_id='%s'"%(session['uid'])
    data['vie']=select(q)   
    return render_template('usersendfbk.html',data=data)


@user.route("/useruploadfiles", methods=['get', 'post'])   
def upfiles():
    if not session.get("lid") is None:
         data = {}
         if 'up' in request.form:
                titl = request.form['tit']
                fil = request.files['file']
                path="static/"+str(uuid.uuid4())+fil.filename
                fil.save(path)
                q = "INSERT INTO `files`(`file_id`,`user_id`,`title`,`file`,`date`) VALUES(NULL,'%s','%s','%s',now())" % (session['uid'], titl, path)
                insert(q)
                return redirect(url_for('user.upfiles'))
    q="select * from files where user_id='%s'"%(session['uid'])
    data['vie']=select(q)   
    return render_template('uploadfiles.html',data=data)


@user.route("/summaryres", methods=['get', 'post'])
def viewres():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM general_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("sumres.html", data=data)


import pyttsx3

@user.route("/text_to_audio", methods=['GET'])
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

@user.route("/highrankres", methods=['get', 'post'])
def viewhighrankres():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM high_rank_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("highrank.html", data=data)

@user.route("/keywordres", methods=['get', 'post'])
def keyres():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM keywords_summary inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("viewkeyword.html", data=data)

@user.route("/simplewordres", methods=['get', 'post'])
def simpleres():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM simple_words_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("viewsimpleres.html", data=data)


@user.route("/keyideares", methods=['get', 'post'])
def ideares():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM gpt_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("viewgptres.html", data=data)


@user.route("/senres", methods=['get', 'post'])
def sentires():
        data = {}
        flid = request.args.get('fid')
        qr = "SELECT * FROM sentiment_analysis_summar inner join files using(file_id) where file_id='%s'"%(flid)
        data['view'] = select(qr)

        return render_template("viewsentires.html", data=data)
   
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
import PyPDF2
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tag import pos_tag
from nltk.chunk import ne_chunk
import nltk
nltk.download('averaged_perceptron_tagger')
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import openai

def general_summary(paragraph):
    sentences = sent_tokenize(paragraph)
    key_sentences = sentences[:3]
    summary = ' '.join(key_sentences)
    return summary  

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

@user.route("/general_summary/", methods=['GET','POST'])
def generate_summary():
    res=""
    data={}
    print('*******************')
    file_id = request.args.get('fid')
    print(file_id)
    
    # Retrieve file path based on file_id
    file_query = "SELECT file FROM files WHERE file_id='%s'"%(file_id)
    file_data = select(file_query)
    print(file_data)
  
    if not file_data:
        return "File not found."

    # Extract file path from the result
    # pdf_path = "C:/Users/LENOVO/Downloads/" + file_data[0]['file']
    pdf_path = "C:/Users/athul/OneDrive/Desktop/New folder (2)/Summary_Generation MES Final Project/summarygen/" + file_data[0]['file']


    # Read file content
    file_content = extract_text_from_pdf(pdf_path)

    # Generate summary
    summary = general_summary(file_content)
    print(summary)

    if summary:
        qry = "SELECT * FROM general_summar WHERE file_id='%s'" %(file_id)
        res = select(qry)
    if not res:
        # insert_query = "INSERT INTO general_summar(general_summary_id, file_id, general_result_summary) VALUES (NULL, '%s', '%s')" % (file_id, summary)
        insert_query = "INSERT INTO general_summar VALUES (NULL, '%s', '%s')" % (file_id, summary)

        insert(insert_query)
    else:
        return redirect(url_for('user.viewres',fid=file_id))
    return render_template('sumres.html',data=data)


def summary_by_high_ranking_words_tfidf(paragraph):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(paragraph)
    filtered_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    high_ranking_words = set(filtered_words[:5])
    
    # Compute TF-IDF vectors
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', vocabulary=high_ranking_words)
    print(tfidf_vectorizer)
    tfidf_matrix = tfidf_vectorizer.fit_transform([paragraph])
    print(tfidf_matrix)

    # Summarize using top TF-IDF weighted sentences
    sentences = paragraph.split('\n')
    print(sentences)
    sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
    print(sentence_scores)
    top_sentences_indices = sentence_scores.argsort()[-3:][::-1]  # Selecting top 3 sentences
    print(top_sentences_indices)
    summary_sentences = [sentences[idx].strip() for idx in top_sentences_indices]
    print(summary_sentences)
    summary = ' '.join(summary_sentences)

    return summary

@user.route("/high_rank_summary/", methods=['GET','POST'])
def generate_high_rank_summary_tfidf():
    data={}
    file_id = request.args.get('fid')
    
    # Retrieve file path based on file_id
    file_query = "SELECT file FROM files WHERE file_id='%s'" % file_id
    file_data = select(file_query)
  
    if not file_data:
        return "File not found." 
  
    # Extract file path from the result
    pdf_path = "C:/Users/athul/OneDrive/Desktop/New folder (2)/Summary_Generation MES Final Project/summarygen/" + file_data[0]['file']

    # Read file content
    file_content = extract_text_from_pdf(pdf_path)

    # Generate summary by high-ranking words using TF-IDF
    summary = summary_by_high_ranking_words_tfidf(file_content)

    if summary:
        qry = "SELECT * FROM high_rank_summar WHERE file_id='%s'" %(file_id)
        res = select(qry)
    if not res:
        insert_query = "INSERT INTO high_rank_summar(high_rank_summary_id, file_id, high_rank_result_summary) VALUES (NULL, '%s', '%s')" % (file_id, summary)
        insert(insert_query)
    else:
        return redirect(url_for('user.viewhighrankres',fid=file_id))
    return render_template('highrank.html',data=data)
    

# def extract_top_keywords(text, num_keywords=5):
#     stop_words = set(stopwords.words('english'))
#     tokens = word_tokenize(text.lower())
#     tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
#     word_freq = Counter(tokens)
#     top_keywords = [word for word, _ in word_freq.most_common(num_keywords)]
#     return top_keywords

# def summary_by_keywords(paragraph, keywords):
#     summary_sentences = [sentence for sentence in sent_tokenize(paragraph) if any(keyword in sentence.lower() for keyword in keywords)]
#     summary = ' '.join(summary_sentences)
#     return summary

@user.route("/summary_by_keywords", methods=['GET','POST'])
def summary_by_keywords():
    print('&&&&&&&&&&&&&&&')
    data={}
    file_id = request.form.get('fid')
    keywords = request.form.get('keywords')


    print("File ID:", file_id)
    print("Keywords:", keywords)

    if not file_id:
        return "File ID not provided."

    if not keywords:
        return "Keywords not provided."
    
    

    file_query = "SELECT file FROM files WHERE file_id='%s'" % file_id
    file_data = select(file_query)
    print(file_data)

    pdf_path = "C:/Users/athul/OneDrive/Desktop/New folder (2)/Summary_Generation MES Final Project/summarygen/" + file_data[0]['file']

    file_content = extract_text_from_pdf(pdf_path)
    print(file_content)

    # Split the keywords provided by the user
    keyword_list = keywords.split()
    print(keyword_list)

    
    # Generate summary sentences containing any of the keywords
    summary_sentences = [sentence for sentence in sent_tokenize(file_content) if any(keyword in sentence.lower() for keyword in keyword_list)]
    
    # Join summary sentences to form the summary
    summary = ' '.join(summary_sentences)
    print(summary)

    qry = "SELECT * FROM keywords_summary WHERE file_id='%s'" %(file_id)
    print(qry)
    res = select(qry)
    if not res:
        insert_query = "INSERT INTO keywords_summary(keywords_summary_id, file_id, keywords_result_summary) VALUES (NULL, '%s', '%s')" % (file_id,summary)
        print(insert_query)
        insert(insert_query)
    else:
        return redirect(url_for('user.keyres', fid=file_id))
    return render_template('viewkeyword.html',data=data)

def summary_in_simple_words(paragraph):
    blob = TextBlob(paragraph)
    simplified_sentences = []
    for sentence in blob.sentences:
        simplified_words = [word.singularize().lower() for word in sentence.words]
        print(simplified_words)
        simplified_sentence = ' '.join(simplified_words)
        simplified_sentences.append(simplified_sentence)
    simplified_summary = ' '.join(simplified_sentences)
    return simplified_summary

@user.route("/by_simplewords/", methods=['GET'])
def generate_summary_in_simple_words():

    data={}
    file_id = request.args.get('fid')

    file_query = "SELECT file FROM files WHERE file_id='%s'" % file_id
    file_data = select(file_query)
    print(file_data)

    if not file_id:
        return "File ID not provided."
    
    pdf_path = "C:/Users/athul/OneDrive/Desktop/New folder (2)/Summary_Generation MES Final Project/summarygen/" + file_data[0]['file']

    file_content = extract_text_from_pdf(pdf_path)

    simple_summary = summary_in_simple_words(file_content)
    simple_summary_string_encoded = simple_summary.replace("'", "''").replace("\n", "\\n")
    # simple_summary_string = tuple(simple_summary)
    # simple_summary_string_encoded = simple_summary_string.encode('utf-8', 'ignore')
    # simple_summary_string_encoded = tuple(simple_summary_string)
    # simple_summary_string_encoded = simple_summary_string.encode(encoding='utf-8', errors='ignore')



    if simple_summary:
        qry = "SELECT * FROM simple_words_summar WHERE file_id='%s'" %(file_id)
        res = select(qry)
    if not res:
        # Ensure that the simple_summary_string is encoded properly
        # simple_summary_string_encoded = simple_summary_string.encode(encoding='utf-8', errors='ignore')
        # simple_summary_string_encoded = mysql.connector.escape_string(simple_summary_string)

        # Construct the insertion query with the properly encoded string
        insert_query = "INSERT INTO simple_words_summar VALUES (NULL, '%s', '%s')" % (file_id, simple_summary_string_encoded)

        # Insert the data into the database
        insert(insert_query)

        

    else:
        return redirect(url_for('user.simpleres',fid=file_id))
    return render_template('viewsimpleres.html',data=data)
    

def sentiment_analysis_summary(paragraph):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(paragraph)['compound']
    print('Sentiment Score:',sentiment_score)
    
    if sentiment_score >= 0.05:
        sentiment = "positive"
    elif sentiment_score <= -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    summary = f"The overall sentiment is {sentiment}. {paragraph}"
    return summary


@user.route("/sentiment_analysis_summary/", methods=['GET'])
def generate_sentiment_analysis_summary():

    data={}
    file_id = request.args.get('fid')

    file_query = "SELECT file FROM files WHERE file_id='%s'" % file_id
    file_data = select(file_query)

    if not file_id:
        return "File ID not provided."
    
    pdf_path = "C:/Users/athul/OneDrive/Desktop/New folder (2)/Summary_Generation MES Final Project/summarygen/" + file_data[0]['file']

    file_content = extract_text_from_pdf(pdf_path)

    sentiment_summary1 = sentiment_analysis_summary(file_content)
    sentiment_summary_string_encoded = sentiment_summary1.replace("'", "''").replace("\n", "\\n")



    qry = "SELECT * FROM sentiment_analysis_summar WHERE file_id='%s'" %(file_id)
    res = select(qry)
    if not res:
        qu = "INSERT INTO sentiment_analysis_summar(sentiment_analysis_summary_id, file_id, sentiment_analysis_result_summary) VALUES (NULL, '%s', '%s')" % (file_id, sentiment_summary_string_encoded)
        insert(qu)
    else:
        return redirect(url_for('user.sentires',fid=file_id))
    return render_template('viewsentires.html',data=data)

def summary_by_key_ideas(paragraph):
    words = word_tokenize(paragraph)
    tagged_words = pos_tag(words)
    named_entities = ne_chunk(tagged_words)

    key_ideas = []
    for chunk in named_entities:
        if hasattr(chunk, 'label') and chunk.label():
            key_ideas.append(' '.join(c[0] for c in chunk.leaves()))

    key_ideas_summary = ', '.join(key_ideas)
    return key_ideas_summary

@user.route("/by_key_ideas/", methods=['GET'])
def generate_gpt_summary_by_key_ideas():

    data={}
    file_id = request.args.get('fid')

    file_query = "SELECT file FROM files WHERE file_id='%s'" % file_id
    file_data = select(file_query)

    if not file_id:
        return "File ID not provided."
    
    pdf_path = "C:/Users/athul/OneDrive/Desktop/New folder (2)/Summary_Generation MES Final Project/summarygen/" + file_data[0]['file']

    # Read file content
    file_content = extract_text_from_pdf(pdf_path)

    # Generate summary by key ideas
    key_ideas_summary = summary_by_key_ideas(file_content)

    qry = "SELECT * FROM gpt_summar WHERE file_id='%s'" %(file_id)
    res = select(qry)
    if not res:
        qu = "INSERT INTO gpt_summar(gpt_summary_id, file_id, gpt_result_summary) VALUES (NULL, '%s', '%s')" % (file_id, key_ideas_summary)
        insert(qu)
    else:
        return redirect(url_for('user.ideares',fid=file_id))
    return render_template('viewgptres.html',data=data)


from transformers import TFGPT2LMHeadModel, GPT2Tokenizer
model_name = "gpt2" 
model = TFGPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)


# Set up the function to generate descriptions
def generate_description(word):
    input_ids = tokenizer.encode(word, return_tensors="pt")
    output = model.generate(input_ids, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text


@user.route("/uploadwrd", methods=['get', 'post'])
def wrd():
    data = {}   
    if 'upl' in request.form:
        word = request.form['wrd']
        
        description = generate_description(word)
        
        q = "INSERT INTO `word`(`word_id`,`user_id`,`word`,`description`,`date`) VALUES(NULL,'%s','%s','%s',now())" % (session['uid'], word, description)
        insert(q)

        q = "SELECT * FROM `word` WHERE `user_id`='%s'" % (session['uid'])
        data['view'] = select(q)
    return render_template('uploadword.html', data=data)

  
@user.route("/ustrans", methods=['GET'])
def translate():
    summary = request.args.get('text')
    return render_template("ustranslate.html",summary=summary)


from googletrans import Translator

@user.route("/translate_summary", methods=["POST"])
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
