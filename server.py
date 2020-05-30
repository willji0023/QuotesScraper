import json
from os import path
from flask import Flask, render_template, redirect, url_for
import webscraper

# Create the application instance
app = Flask(__name__, template_folder="templates")


def json_to_dict(path):
    with open(path, "r") as infile:
        data = json.loads(infile.read())
        infile.close()
        return data


# Create a URL route in our application for "/"
@app.route("/")
def index():
    quote_data = None
    while quote_data is None:
        try: 
            quote_data = json_to_dict("QuoteData.json")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            webscraper.main()
            print("Decoding JSON has failed")
    image_url = (
        open("image_url.txt", "r").read()
        if path.exists("image_url.txt")
        else webscraper.FAILSAFE_IMAGE
    )
    print(image_url)
    return render_template(
        "index.html",
        text=quote_data.get("text"),
        author=quote_data.get("author"),
        title=quote_data.get("title"),
        url=image_url,
    )


@app.route("/background_process")
def background_process():
    webscraper.main()
    return "."


if __name__ == "__main__":
    app.run(debug=True)
