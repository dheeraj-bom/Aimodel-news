'''from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load the saved trained model and TF-IDF Vectorizer
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("tfidf.pkl", "rb") as tfidf_file:
    tfidf = pickle.load(tfidf_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    title = request.form['title']
    description = request.form['description']
    combined_text = title + " " + description
    transformed_text = tfidf.transform([combined_text])
    category = model.predict(transformed_text)

    # Convert category to a standard Python int
    category = int(category[0])

    # Placeholder for tag prediction logic
    tags = ["Tag1", "Tag2"]  # Replace with actual tag prediction logic

    # Determine if it's breaking news or not
    news_type = "Breaking" if "breaking" in title.lower() else "Normal"

    return jsonify({
        'category': category,
        'tags': tags,
        'type': news_type
    })

if __name__ == "__main__":
    app.run(debug=True)'''
    #=============================================================================
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load the trained model and TF-IDF vectorizer
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("tfidf.pkl", "rb") as tfidf_file:
    tfidf = pickle.load(tfidf_file)

# Define categories
categories = {0: 'ARTS & CULTURE', 1: 'BUSINESS', 2: 'COMEDY', 3: 'CRIME', 4: 'EDUCATION',
               5: 'ENTERTAINMENT', 6: 'ENVIRONMENT', 7: 'MEDIA', 8: 'POLITICS', 9: 'RELIGION',
               10: 'SCIENCE', 11: 'SPORTS', 12: 'TECH', 13: 'WOMEN'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    title = request.form.get('title', '')
    body = request.form.get('body', '')
    
    if not title or not body:
        return jsonify({'error': 'Title and body are required.'}), 400

    # Preprocess and predict
    text = title + " " + body
    text_vectorized = tfidf.transform([text])
    prediction = model.predict(text_vectorized)
    
    # Return results
    result = {
        'Category': categories[int(prediction[0])],
        'Type'    : 'Breaking' if 'breaking' in text.lower() else 'Normal'
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

