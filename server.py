import json
from flask import Flask, render_template
import webscraper

# Create the application instance
app = Flask(__name__, template_folder='templates')

def json_to_dict(path):
    with open(path, 'r') as infile:
        data = json.loads(infile.read())
        infile.close()
        return data

# Create a URL route in our application for "/"
@app.route('/')
def index():
    quote_data = json_to_dict('QuoteData.json')
    return render_template('index.html', text=quote_data.get("text"), author=quote_data.get("author"), title=quote_data.get("title"))

@app.route('/background_process')
def background_process():
    webscraper.main()
    return (".")

if __name__ == '__main__':
    app.run(debug=True)
