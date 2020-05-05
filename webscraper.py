from bs4 import BeautifulSoup, NavigableString
import requests, random

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


class Quote:
    def __init__(self, text, author, title, tags, likes):
        self.text = text
        self.author = author
        self.title = title
        self.tags = tags
        self.likes = likes

    def __repr__(self):
        return f"{self.text} — {self.author}, {self.title}\n Tags: {self.tags}\n {self.likes} have liked this\n\n"


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

    print(repr(quoteObject))
