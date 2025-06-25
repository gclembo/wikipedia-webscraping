import requests, json
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

NUMBER_OF_PAGES = 3

def get_random_page_info():
    url = "https://en.wikipedia.org/wiki/Special:Random"

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    article_content = soup.find("div", id="bodyContent")

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

    return {
        "url": page.url, "title": soup.title.text[:-12],
        "word_count": len(article_content.get_text(separator=" ", strip=True).split()),
        "image_count": num_imgs, "source_count": num_sources,
        "published": publish_date, "modified": modified_date
    }

# Scrape Sites
data = []
for i in range(NUMBER_OF_PAGES):
    entry = get_random_page_info()
    data.append(entry)

# Save data as dataframe
df = pd.DataFrame(data)

file_path = Path(__file__)
project_folder = file_path.resolve().parent.parent
data_folder = str(project_folder) + "\\data"
df.to_csv(data_folder + "\\data.csv", index=False)
