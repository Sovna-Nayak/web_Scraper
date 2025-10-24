import requests
from bs4 import BeautifulSoup
import json
import time
import os

# -----------------------------------------------------------
# 1️⃣  CONFIGURATION
# -----------------------------------------------------------
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0"}
OUTPUT_JSON = "data/books.json"

# Create 'data' folder automatically if it doesn’t exist
os.makedirs("data", exist_ok=True)


# -----------------------------------------------------------
# 2️⃣  SCRAPE A SINGLE PAGE FUNCTION
# -----------------------------------------------------------
def scrape_page(page_number):
    """
    Scrapes one page of book data and returns a list of dictionaries.
    Each dictionary contains: title, price, and link.
    """
    url = BASE_URL.format(page_number)
    response = requests.get(url, headers=HEADERS)

    # If website doesn’t respond correctly, stop scraping
    if response.status_code != 200:
        print(f"⚠️ Failed to retrieve page {page_number}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    books = []

    # Extract book details
    for book in soup.find_all("article", class_="product_pod"):
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip()
        link = "http://books.toscrape.com/catalogue/" + book.h3.a["href"]

        books.append({
            "title": title,
            "price": price,
            "link": link
        })

    return books


# -----------------------------------------------------------
# 3️⃣  MAIN SCRAPER FUNCTION
# -----------------------------------------------------------
def main():
    """
    Loops through all pages and saves results into a JSON file.
    """
    all_books = []
    page_number = 1

    print("🚀 Starting web scraping...")

    while True:
        print(f"📄 Scraping page {page_number}...")
        books = scrape_page(page_number)

        # Stop when no more books found
        if not books:
            print("✅ No more pages found. Exiting.")
            break

        all_books.extend(books)
        page_number += 1
        time.sleep(1)  # Sleep between requests to be polite

    # Save all data as JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=4, ensure_ascii=False)

    print(f"\n🎉 Scraping complete!")
    print(f"📁 Data saved to: {OUTPUT_JSON}")


# -----------------------------------------------------------
# 4️⃣  ENTRY POINT
# -----------------------------------------------------------
if __name__ == "__main__":
    main()




# import requests
# from bs4 import BeautifulSoup
# import pandas as pd
# import json
# import time
# import os

# # ---------------------------
# # CONFIGURATION
# # ---------------------------
# BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
# HEADERS = {"User-Agent": "Mozilla/5.0"}
# #OUTPUT_CSV = "data/books.csv"
# OUTPUT_JSON = "data/books.json"
# os.makedirs("data", exist_ok=True)

# # ---------------------------
# # SCRAPE SINGLE PAGE
# # ---------------------------
# def scrape_page(page_number):
#     url = BASE_URL.format(page_number)
#     response = requests.get(url, headers=HEADERS)
#     if response.status_code != 200:
#         print(f"Failed to retrieve page {page_number}")
#         return []

#     soup = BeautifulSoup(response.text, "html.parser")
#     books = []

#     # Each book item
#     for book in soup.find_all("article", class_="product_pod"):
#         title = book.h3.a["title"]
#         price = book.find("p", class_="price_color").text.strip()
#         link = "http://books.toscrape.com/catalogue/" + book.h3.a["href"]
#         books.append({
#             "title": title,
#             "price": price,
#             "link": link
#         })
#     return books

# # ---------------------------
# # MAIN FUNCTION
# # ---------------------------
# def main():
#     all_books = []
#     page_number = 1

#     print("Starting web scraping...")

#     while True:
#         print(f"Scraping page {page_number}...")
#         books = scrape_page(page_number)
#         if not books:
#             print("No more pages found. Exiting.")
#             break
#         all_books.extend(books)
#         page_number += 1
#         time.sleep(1)  # Be polite to the server

#     # Convert to DataFrame
#     df = pd.DataFrame(all_books)

#     # Save as CSV and JSON
#     df.to_csv(OUTPUT_CSV, index=False)
#     with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
#         json.dump(all_books, f, indent=4, ensure_ascii=False)

#     print(f"✅ Scraping complete! Data saved to:\n- {OUTPUT_CSV}\n- {OUTPUT_JSON}")

# # ---------------------------
# # ENTRY POINT
# # ---------------------------
# if __name__ == "__main__":
#     main()
