import requests
from bs4 import BeautifulSoup
import re
from collections import Counter
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')


# Function to scrape lyrics from a given URL
def scrape_lyrics(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        lyrics = soup.find("div", class_="lyrics").get_text()
        # Clean the lyrics
        lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)  # Remove text within brackets
        lyrics = re.sub(r'\n{2,}', ' ', lyrics)  # Replace multiple newlines with a single space
        lyrics = re.sub(r'\'', '', lyrics)  # Remove apostrophes
        return lyrics.lower()
    except Exception as e:
        return "Error in scraping: " + str(e)


# URLs of popular songs by male and female artists
urls_male = [
    "https://genius.com/Ed-sheeran-shape-of-you-lyrics",
    "https://genius.com/Justin-bieber-yummy-lyrics",
    "https://genius.com/Shawn-mendes-stitches-lyrics"
]

urls_female = [
    "https://genius.com/Adele-hello-lyrics",
    "https://genius.com/Taylor-swift-lover-lyrics",
    "https://genius.com/Ariana-grande-thank-u-next-lyrics"
]

# Scrape lyrics from the URLs
lyrics_male = ' '.join([scrape_lyrics(url) for url in urls_male])
lyrics_female = ' '.join([scrape_lyrics(url) for url in urls_female])


# Function to analyze the frequency of words in lyrics
def analyze_lyrics(lyrics):
    words = re.findall(r'\b[a-z]+\b', lyrics)
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    word_freq = Counter(filtered_words)
    return word_freq.most_common(10)


# Analyze the most common words in male and female lyrics
common_words_male = analyze_lyrics(lyrics_male)
common_words_female = analyze_lyrics(lyrics_female)

common_words_male, common_words_female

