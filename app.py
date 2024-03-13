from flask import Flask, request, jsonify, render_template
import instaloader
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
nltk.download('vader_lexicon')
USER="canakevsk"
PASSWORD="Jabir@7860@53"
app = Flask(__name__)
def negative_comments(allcomments):
    sentiments = []
    sid = SentimentIntensityAnalyzer()
    for comment in allcomments:
        sentiment_scores = sid.polarity_scores(comment)
        if sentiment_scores['compound'] > 0:
            sentiment = 'Positive'
        elif sentiment_scores['compound'] < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        sentiments.append(sentiment)

    # Create a DataFrame to store comments and their sentiments
    data = {'Comment': allcomments, 'Sentiment': sentiments}
    df = pd.DataFrame(data)

    # Filter out negative comments
    negative_comments = df[df['Sentiment'] == 'Negative']

    return negative_comments['Comment'].tolist()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search', methods=['POST'])
def search():
    username = request.form['username']
  
    # Get instance
    loader = instaloader.Instaloader()

    # Login using the credentials
    loader.login(USER, PASSWORD)
    profile = instaloader.Profile.from_username(loader.context,username)
    j=0
    allcomments=[] # to store all commnets 
    for post in profile.get_posts():
        print(f"Post {post.url}")
        print(f"Caption: {post.caption}")
        comments = post.get_comments()
        for comment in comments:
            allcomments.append(str(comment.text)) # to store
            print(comment.text)
            j+=1
            if(j==100):
                break
        break
    negative=negative_comments(allcomments)
    return render_template('index.html',comments=negative)
if __name__ == '__main__':
    app.run(debug=True)