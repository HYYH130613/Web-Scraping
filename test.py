from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


MAIN_URL = "https://pja.edu.pl"

LINK_SELECTOR = "li a" 
CONTENT_SELECTOR = "p"

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10) 
title_level_list = [1, 2, 3, 4, 5,6,7,8,9,10]
titles = []


def parse_page(url, page_name):
    """Navigates to a URL and extracts basic information."""
    print(f"\n--- Parsing: {page_name} ({url}) ---")
    try:
        driver.get(url)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


        page_title = driver.title
        print(f"Page Title: {page_title}")

        # try:
        
        #     first_paragraph = driver.find_element(By.CSS_SELECTOR, CONTENT_SELECTOR)
        #     print(f"Sample Content: {first_paragraph.text}...") # Print first 150 chars
        # except NoSuchElementException:
        #     print("Sample Content: No paragraph found with selector.")


        try:
            for title_level in title_level_list:
                title_elements = driver.find_elements(By.CSS_SELECTOR, f"h{title_level}")

                for title_element in title_elements:
                    tag = title_element.tag_name
                    text = title_element.text

                    title = {
                        "tag": tag,
                        "title": text,
                    }
                    titles.append(title)
            print(titles)
        except NoSuchElementException:
            print("Main content div not found.")

    except TimeoutException:
        print(f"Error: Timeout loading {url}")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Main script ---
try:
    print(f"Navigating to main page: {MAIN_URL}")
    driver.get(MAIN_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 2. Find all links on the main page (this will be many!)
    #    You need a more specific way to identify the links you want.
    #    For example, links in the main navigation menu.
    print("Looking for links...")

    all_links = driver.find_elements(By.CSS_SELECTOR, LINK_SELECTOR)


    pages_to_parse = {}
    for link in all_links:
        url = link.get_attribute('href')
        link_text = link.text.strip()
        # Filter links: must be internal, have text, and not be empty
        if url and url.startswith(MAIN_URL) and url != MAIN_URL:
            # Use link text as a name, or a generic one if text is too long/short
            page_name = link_text if link_text and len(link_text) < 50 else url.split('/')[-2] or 'Page'
            pages_to_parse[url] = page_name

    print(f"Found {len(pages_to_parse)} potential internal pages to parse based on links.")


    count = 0
    for url, name in pages_to_parse.items():
        if count >= 16: 
            print("\nReached test limit of 16 pages. Stopping.")
            break
        parse_page(url, name)
        time.sleep(2) 
        count += 1

finally:

    driver.quit()
    print("\nBrowser closed.")
    
# title_level_list = [1, 2, 3, 4, 5,6,7,8,9,10]
# k = 0
# for i in url:
    
#     driver.get(i)
#     titles = []

#     for title_level in title_level_list:
#         title_elements = driver.find_elements(By.CSS_SELECTOR, f"h{title_level}")

#         for title_element in title_elements:
#             tag = title_element.tag_name
#             text = title_element.text

#             title = {
#                 "tag": tag,
#                 "title": text,
#             }
#             titles.append(title)
#     with open(f"titles{k}.csv", mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.DictWriter(file, fieldnames=["tag", "title"])
#         writer.writeheader()

#         for row in titles:
#             writer.writerow(row)
#     k+=1


# driver.quit()