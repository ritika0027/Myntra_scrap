###Myntra Purse Scraper:


**Overview**

This Python script is designed to scrape purse product details from the Myntra website using Selenium and BeautifulSoup. It extracts information such as brand, product name, prices, ratings, reviews, material, availability, seller, and product URL.

----

**Features**

Scrapes purse listings from Myntra, sorted by price (ascending).

Navigates multiple pages to collect product details.

Extracts and stores product information in a structured format.

Saves the data into a CSV file (``myntra_purses.csv``).

Runs in headless mode for efficiency.

Handles pagination and avoids duplicate links.

---

**Technologies Used**

Python

Selenium

BeautifulSoup

Pandas

WebDriver Manager

****Installation****

**Prerequisites**

Ensure you have the following installed on your system:

Python 3.x

Google Chrome browser

----

**Install Dependencies**

Use the following command to install the required Python packages:

pip install selenium pandas beautifulsoup4 webdriver-manager

----

**Usage**

Clone the repository:

``git clone https://github.com/your-username/myntra-purse-scraper.git``
``cd myntra-purse-scraper``

Run the script:

``python scraper.py``

The scraped data will be saved in ``myntra_purses.csv``.

---

**Output**

The script generates a CSV file with the following columns:

Brand

Product Name

Discounted Price

Original Price

Rating

Reviews

Material

Availability

Seller

Product URL

---

**Notes**

The script runs in headless mode to avoid opening the browser UI.

Myntra's structure may change over time, requiring script updates.

Running multiple requests in a short time may trigger bot detection.

----

**License**

This project is licensed under the MIT License.

---

**Disclaimer**

This project is for educational purposes only. Scraping websites without permission may violate their terms of service. Use responsibly.

