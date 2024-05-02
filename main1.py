from flask import Flask, render_template, request
import pickle
import nltk
import twitterbot2 as tb
from nltk.tokenize import TweetTokenizer, sent_tokenize
from nltk.corpus import stopwords, opinion_lexicon
from nltk.stem.wordnet import WordNetLemmatizer
import re, string
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import matplotlib
from selenium import webdriver

import psycopg2
matplotlib.use('Agg')  # Switch to non-interactive backend


app = Flask(__name__)

# Load the trained classifier from the pickle file
with open('sentiment_classifier.pickle', 'rb') as file:
    classifier = pickle.load(file)

# Initialize NLTK resources
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('opinion_lexicon')

tk = TweetTokenizer()
STOP_WORDS = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Load positive and negative words
positive_words = set(opinion_lexicon.positive())
negative_words = set(opinion_lexicon.negative())

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="dpg-cnleda8l5elc73dq8j0g-a",
    database="country_5aym",
    user="amit",
    password="J6O5kkf7wCcsGeN7XAgKWbL4rsMves0W"
)
VIEW_DATA_PASSWORD = "amit"

# Create a cursor
cur = conn.cursor()

# Define function to preprocess input text and count positive and negative words
def preprocess_text(tweet_text):
    # Tokenize
    tokens = tk.tokenize(tweet_text)
    
    # Remove noise
    cleaned_tokens = []
    positive_count = 0
    negative_count = 0
    for token in tokens:
        # Remove URLs, 
        token = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        # remove the words which start @
        token = re.sub(r'@[A-Za-z0-9_]+', '', token)
         # remove the words which start #
        token = re.sub(r'#[A-Za-z0-9_]+', '', token)
        # Lemmatize
        token = lemmatizer.lemmatize(token.lower())
        # Remove stopwords, punctuation, and short words
        if token not in STOP_WORDS and token not in string.punctuation and len(token) > 2:
            cleaned_tokens.append(token)
            if token in positive_words:
                positive_count += 1
            elif token in negative_words:
                negative_count += 1
    return cleaned_tokens, positive_count, negative_count

# Create table to store analysis results
cur.execute('''
    CREATE TABLE IF NOT EXISTS analysis_results (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        text TEXT,
        cleaned_text TEXT,
        total_words INT,
        total_sentences INT,
        positive_words INT,
        negative_words INT,
        sentiment VARCHAR(10)
    )
''')
conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        URL = request.form['URL']
        bot = tb.Twitterbot()

        tweet_text = bot.open_a_twitter_link(URL, 1000)
        
        name=request.form["name"]
        
        # Preprocess the input text and count positive and negative words
        processed_text, positive_count, negative_count = preprocess_text(tweet_text)
        cleaned_text = ' '.join(processed_text)
        
        # Calculate total number of words
        total_words = len(processed_text)
        
        # Calculate total number of sentences
        total_sentences = len(sent_tokenize(tweet_text))
        
         # Classify the processed text
        prediction = classifier.classify(dict([token, True] for token in processed_text))
        
        # Determine sentiment label
        sentiment = "Negative" if prediction == 0 else "Positive"
        
        # Insert analysis results into the PostgreSQL table
        cur.execute('''
            INSERT INTO analysis_results (name, text, cleaned_text, total_words, total_sentences, positive_words, negative_words, sentiment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (name, tweet_text, cleaned_text, total_words, total_sentences, positive_count, negative_count, sentiment))
        conn.commit()
        
        # Generate bar graph
        plt.figure(figsize=(8, 6))
        plt.bar(['Total Words', 'Total Sentences', 'Positive Words', 'Negative Words'], 
                [total_words, total_sentences, positive_count, negative_count])
        plt.ylabel('Count')
        plt.title('Text Analysis')
        
        # Convert plot to base64 image
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()
        
        return render_template('result.html', name=name,tweet_text=tweet_text, cleaned_text=cleaned_text, sentiment=sentiment,
        positive_count=positive_count, negative_count=negative_count,
        image_base64=image_base64)


@app.route('/admin')
def admin():
    return render_template("admin.html")

# this code for show the postgres table after submit admin password
@app.route('/view_data', methods=['POST'])
def view_data():
    password_attempt = request.form['password']
    if password_attempt == VIEW_DATA_PASSWORD:

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM analysis_results")
        data = cursor.fetchall()

        return render_template('detail.html', data=data)
    else:
        return "Incorrect password. Access denied."

if __name__ == '__main__':
    app.run(debug=True)
