import re
from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://sayak5913:oOqfiWXHb9Cbayli@cluster0.2x4xrqw.mongodb.net/space_news?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]+', '-', text.lower()).strip('-')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add_article', methods=['GET','POST'])
def add_article():
    message = ''
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        slug = slugify(title)
        
        if title and content:
            article = {"title": title, "content": content, "slug": slug}
            mongo.db.articles.insert_one(article)
            message = "Article submitted successfully!"
        else:
            message = "Please fill in all fields."

    return render_template('index.html', message=message)

@app.route('/get_articles', methods=['GET'])
def get_articles():

    articles = list(mongo.db.articles.find())
    for article in articles:
            article["_id"] = str(article["_id"])

    return jsonify(articles[::-1])

@app.route('/get_article/<slug>')
def get_article(slug):
    print(id)
    article = mongo.db.articles.find_one({"slug": slug})
    if article:
        return jsonify({
            "_id": str(article["_id"]),
            "title": article["title"],
            "content": article["content"]
        })
    else:
        return jsonify({"error": "Article not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
