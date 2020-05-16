from flask import Flask, render_template, request
import webscraper

# Create the application instance
app = Flask(__name__, template_folder='templates')

# Create a URL route in our application for "/"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/background_process')
def background_process():
    webscraper.main()
    return (".")

if __name__ == '__main__':
    app.run(debug=True)
