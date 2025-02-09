import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from selenium.webdriver.common.action_chains import ActionChains


def remove_duplicates(lst):
    seen = set()
    unique_list = []
    for item in lst:
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return unique_list


# Myntra Search URL for Purses (First Page) sorted by popularity
# myntra_url = "https://www.myntra.com/purses?sort=popularity"
myntra_url = "https://www.myntra.com/purses?sort=price_asc"

# Set Chrome Options (Headless Mode)
options = Options()
options.add_argument("--headless")  # Run in the background
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920, 1080")
options.add_argument("--blink-settings=imagesEnabled=true")


# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(myntra_url)
time.sleep(10)

# Extract Purse Listings
purses = []

# Loop through multiple pages
product_links = []
page = 1

original_tab = driver.current_window_handle

while True:

    print(f"📄 Scraping Page {page}...")
    elements = driver.find_elements(By.CLASS_NAME, "product-base")

    for index in range(len(elements)):
        elements = driver.find_elements(By.CLASS_NAME, "product-base")
        print(f"Opening -----> page {page} : element {index + 1}")
        element_click = elements[index]
        # ActionChains(driver).move_to_element(element_click).click().perform()
        element_click.click()
        time.sleep(3)

        driver.switch_to.window(driver.window_handles[-1])

        page_url = driver.current_url
        print(f"Page url : {page_url}")
        product_links.append(page_url)

        driver.close()
        driver.switch_to.window(original_tab)

        time.sleep(3)

    try:
        # time.sleep(30)
        next_button = driver.find_element(By.CLASS_NAME, 'pagination-next')
        ActionChains(driver).move_to_element(next_button).click().perform()
        
        page += 1
        time.sleep(10)

    except:
        print("🚫 No more pages to scrape.")
        break

len_before = len(product_links)
product_links = remove_duplicates(product_links)
len_after = len(product_links)
print(f"Number of links: {len_before} ----> {len_after}")

lnk_no = 1
for lnk in product_links:

    try:
        driver.get(lnk)
        time.sleep(3)  # Allow page to load

        print(f"Opening -----> [{lnk_no}] link : ({lnk})")

        product_soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract Product Details
        brand = product_soup.find("h1", class_="pdp-title").text.strip() if product_soup.find("h1", class_="pdp-title") else "N/A"
        name = product_soup.find("h1", class_="pdp-name").text.strip() if product_soup.find("h1", class_="pdp-name") else "N/A"
        discounted_price = product_soup.find("span", class_="pdp-price").text.strip() if product_soup.find("span", class_="pdp-price") else "N/A"
        original_price = product_soup.find("span", class_="pdp-mrp").text.strip() if product_soup.find("span", class_="pdp-mrp") else "N/A"

        rating = product_soup.find("div", class_="index-overallRating")
        review_count = product_soup.find("div", class_="index-ratingsCount")
        material_info = product_soup.find_all('p', class_='pdp-sizeFitDescContent pdp-product-description-content')
        stock_info = product_soup.find("div", class_="pdp-price-info")
        seller_info = product_soup.find("span", class_="SelectedSizeSellerInfo-sellerButton")

        # Assign extracted values safely
        product_rating = rating.text.strip() if rating else "N/A"
        product_reviews = review_count.text.strip() if review_count else "N/A"

        # material = material_info[1].text.strip() if len(material_info) > 1 else "N/A"
        material = material_info[1].contents[0].strip() if len(material_info) > 1 else "N/A"

        availability = "In Stock" if stock_info else "Out of Stock"
        seller = seller_info.text.strip() if seller_info else "N/A"


        purses.append([brand, name, discounted_price, original_price, product_rating, product_reviews, material, availability, seller, lnk])

    except Exception as e:
            print(f"⚠️ Error scraping product -----> [{lnk_no}] link : ({lnk})")

    lnk_no +=1




# Close WebDriver
driver.quit()

# Convert to DataFrame
df = pd.DataFrame(purses, columns=["Brand", "Product Name", "Discounted Price", "Original Price", "Rating", "Reviews", "Material", "Availability", "Seller", "Product URL"])

# Save to CSV
df.to_csv("myntra_purses.csv", index=False)

print("✅ Scraping Complete! Data saved to 'myntra_purses.csv'")
