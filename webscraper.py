from bs4 import BeautifulSoup, NavigableString
import requests, random, json
from googleapiclient.discovery import build
import urllib.request

# HTML Element Constants
QUOTE_TAG = "div"
TEXT_TAG = "div"
AUTHOR_TAG = "span"
TITLE_TAG = "a"
TAGS_TAB_TAG = "div"
TAGS_TAG = "a"
LIKES_TAG = "a"

ATTRIBUTE_NAME = "class"

QUOTE_ATTRIBUTE_VALUE = "quote"
TEXT_ATTRIBUTE_VALUE = "quoteText"
AUTHOR_ATTRIBUTE_VALUE = "authorOrTitle"
TITLE_ATTRIBUTE_VALUE = "authorOrTitle"
TAGS_ATTRIBUTE_VALUE = "greyText smallText left"
LIKES_ATTRIBUTE_VALUE = "smallText"

page_number = random.randrange(1, 100)
url = f"https://www.goodreads.com/quotes?page={page_number}"
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

# Google API Constants
DEVELOPER_KEY = "AIzaSyCo3KuiiDCvdoHo2nIGbOzjhHO8k1eyCDg"
CX_ID = "016656735448507306327:vgjz9dha2wj"

# Image 
FAILSAFE_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/7/70/Solid_white.svg"

# Search Google custom search for a picture relating to image topic and save in images/
def download_image(image_topic):
    service = build("customsearch", "v1", developerKey=DEVELOPER_KEY)
    res = service.cse().list(
        q = image_topic,
        cx = CX_ID,
        searchType='image',
        num=1,
        fileType='png',
        safe= 'off'
    ).execute()
    for item in res['items']: # TODO: Figure a better way to parse res that doesn't require a loop
        try:
            urllib.request.urlretrieve(item['link'], "static/images/quote_bg.png")
        except:
            urllib.request.urlretrieve(FAILSAFE_IMAGE, "static/images/quote_bg.png")

class Quote:
    def __init__(self, text, author, title, tags, likes):
        self.text = text
        self.author = author
        self.title = title
        self.tags = tags
        self.likes = likes

    def __repr__(self):
        return f"{self.text} — {self.author}, {self.title}\n Tags: {self.tags}\n {self.likes} have liked this\n\n"

def main(args=""):
    quote_arr = []
    for quote in content.find_all(QUOTE_TAG, attrs={ATTRIBUTE_NAME: QUOTE_ATTRIBUTE_VALUE}):
        quote_contents = quote.find(TEXT_TAG, attrs={ATTRIBUTE_NAME: TEXT_ATTRIBUTE_VALUE})
        text = ""
        for c in quote_contents:
            # Emdash = end of quote
            if "―" in str(c):
                # TODO: Find a better way to this
                # If content has both the emdash and the rest of the quote in seperate lines, parse for the quote
                if "<br/>" in str(c):
                    text += str(c)[: str(c).find("<br/>")].replace("<br>", "\n")
                break
            elif not c.find("br"):
                continue
            text += str(c).lstrip()

        title = (
            quote.find(
                TITLE_TAG, attrs={ATTRIBUTE_NAME: TITLE_ATTRIBUTE_VALUE}
            ).text.strip()
            if quote.find(TITLE_TAG, attrs={ATTRIBUTE_NAME: TITLE_ATTRIBUTE_VALUE}) != None
            else ""
        )

        tags = (
            [
                tag.text.strip()
                for tag in quote.find(
                    TAGS_TAB_TAG, attrs={ATTRIBUTE_NAME: TAGS_ATTRIBUTE_VALUE}
                ).find_all(TAGS_TAG)
            ]
            if quote.find(TAGS_TAB_TAG, attrs={ATTRIBUTE_NAME: TAGS_ATTRIBUTE_VALUE})
            != None
            else []
        )

        quoteObject = Quote(
            text,
            quote.find(AUTHOR_TAG, attrs={ATTRIBUTE_NAME: AUTHOR_ATTRIBUTE_VALUE})
            .text.strip()
            .rstrip(","),
            title,
            tags,
            quote.find(LIKES_TAG, attrs={ATTRIBUTE_NAME: LIKES_ATTRIBUTE_VALUE})
            .text.strip()
            .rstrip(" likes"),
        )
        
        quote_arr.append(quoteObject)

    random_quote = quote_arr[random.randrange(0, len(quote_arr) - 1)]
    print(repr(random_quote))
    with open('QuoteData.json', 'w+') as outfile:
        json.dump(random_quote.__dict__, outfile)
        outfile.close()

    image_topic = (
        # " ".join(random_quote.tags) <- Not used because images w/ text become common
        random_quote.tags[random.randint(0, len(random_quote.tags)) - 1]
        if random_quote.tags
        else "white"
    )
    print(image_topic)
    download_image(image_topic) 
