from search_engine.word_calculations import Page, SearchEngine
import requests, json, sqlite3, pickle
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

NUMBER_OF_PAGES = 1000


def process_random_page_info():
    url = "https://en.wikipedia.org/wiki/Special:Random"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    article_content = soup.find("div", id="bodyContent")

    title = soup.title.text[:-12]
    # print(soup.title.text)
    # print(page.url)

    #words and images
    # print("Word Count", len(article_content.get_text(separator=" ", strip=True).split()))

    images = article_content.find_all("img")
    num_imgs = len(images)
    # print("Image Count", num_imgs)

    # sources
    num_sources = 0
    source_sections = article_content.find_all("ol", class_="references")
    if len(source_sections) > 0:
        num_sources = len(source_sections[-1].find_all("li", recursive=False))
    # print("Source Count", num_sources)

    # dates
    publish_date = None
    modified_date = None
    other_json = soup.find("script", type="application/ld+json")
    if other_json is not None:
        other_info = json.loads(other_json.text)

        key_set = other_info.keys()
        if "datePublished" in key_set:
            publish_date = other_info["datePublished"]

        if "dateModified" in key_set:
            modified_date = other_info["dateModified"]

    # print("Published", publish_date)
    # print("Last Modified", modified_date)


    page_text = article_content.get_text(separator=" ", strip=True)

    my_page = Page(title, page.url, page_text)

    return {
        "url": page.url, "title": title,
        "word_count": len(page_text.lower().split()),
        "image_count": num_imgs, "source_count": num_sources,
        "published": publish_date, "modified": modified_date
    }, my_page


# Scrape Sites
data = []
pages = []

for i in range(NUMBER_OF_PAGES):
    entry, my_page = process_random_page_info()
    data.append(entry)
    pages.append(my_page)
    if i % 10 == 0:
        print(str(i + 1) + " Pages Scraped")
print("Done Scraping")

# Save data
df = pd.DataFrame(data)
df["published"] = pd.to_datetime(df["published"])
df["modified"] = pd.to_datetime(df["modified"])


file_path = Path(__file__)
project_folder = file_path.resolve().parent.parent
data_folder = project_folder / "data"

# Database
db_filename = "wiki_data.db"
conn = sqlite3.connect(data_folder / db_filename)
df.to_sql("pages_raw", conn, if_exists="replace", index=False)
conn.close()

# Search Engine
wiki_engine = SearchEngine(pages)

with open(data_folder / "search_engine.pickle", "wb") as file:
    pickle.dump(wiki_engine, file, protocol=5)