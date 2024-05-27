import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
import json
import random
from flask import Flask, render_template, request

# Load mô hình và dữ liệu
model = load_model('model.h5')
with open('data.json', encoding='utf-8') as file:
    intents = json.load(file)
words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))

# Load dữ liệu tin tức
with open('news_data.json', encoding='utf-8') as file:
    news_data = json.load(file)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result
    
def chatbot_response(msg):
    if 'tin tức hôm nay' in msg.lower():
        random.shuffle(news_data['intents'])  # Xáo trộn danh sách tin tức
        news_responses = []
        for news in news_data['intents']:
            title = news['tag']
            summary = news['patterns'][0]
            link = news['responses'][0].split()[-1]
            news_responses.append(f"<strong>Tiêu đề:</strong> {title}<br><strong>Nội dung:</strong> {summary}<br><a href='{link}' target='_blank'>Xem thêm</a><br><br>")
            break 
        return "".join(news_responses)

    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return chatbot_response(userText)

if __name__ == "__main__":
    app.run(debug=True)

