# Importing libraries
from bs4 import BeautifulSoup
import requests

def main(URL):
    # specifying user agent
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    # Making the HTTP Request
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")

    # Retrieving product title
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_string = title.string.strip().replace(',', '') if title else "NA"
    except AttributeError:
        title_string = "NA"
    print("Product Title:", title_string)

    # Retrieving price
    try:
        price_tag = soup.find("span", attrs={'id': 'priceblock_ourprice'})
        price = price_tag.string.strip().replace(',', '') if price_tag else "NA"
    except AttributeError:
        price = "NA"
    print("Product Price:", price)

    # Retrieving product rating
    try:
        rating_tag = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'})
        rating = rating_tag.string.strip().replace(',', '') if rating_tag else "NA"
    except AttributeError:
        try:
            rating_tag = soup.find("span", attrs={'class': 'a-icon-alt'})
            rating = rating_tag.string.strip().replace(',', '') if rating_tag else "NA"
        except:
            rating = "NA"
    print("Overall Rating:", rating)

    # Retrieving total reviews
    try:
        review_tag = soup.find("span", attrs={'id': 'acrCustomerReviewText'})
        review_count = review_tag.string.strip().replace(',', '') if review_tag else "NA"
    except AttributeError:
        review_count = "NA"
    print("Total Reviews:", review_count)

    # Retrieving availability status
    try:
        available_tag = soup.find("div", attrs={'id': 'availability'})
        available_span = available_tag.find("span") if available_tag else None
        available = available_span.string.strip().replace(',', '') if available_span else "NA"
    except AttributeError:
        available = "NA"
    print("Availability:", available)

    # Saving data to CSV
    with open("out.csv", "a") as File:
        File.write(f"{title_string},{price},{rating},{review_count},{available}\n")


if __name__ == '__main__':
    # Reading URLs from the file
    with open("url.txt", "r") as file:
        for links in file.readlines():
            main(links.strip())  # Remove newlines from URLs
