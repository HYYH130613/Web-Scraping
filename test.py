from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


MAIN_URL = "https://pja.edu.pl"

LINK_SELECTOR = "a" # Selects all links - adjust for better targeting!
CONTENT_SELECTOR = "p" # Selects paragraphs for sample content

driver = webdriver.Chrome() 
driver.maximize_window()
wait = WebDriverWait(driver, 10) # Maximum wait time of 10 seconds

def parse_page(url, page_name):
    """Navigates to a URL and extracts basic information."""
    print(f"\n--- Parsing: {page_name} ({url}) ---")
    try:
        driver.get(url)
        # Wait for the body to load to ensure the page is rendered
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Get the page title
        page_title = driver.title
        print(f"Page Title: {page_title}")

        try:
            # Find the first paragraph element
            first_paragraph = driver.find_element(By.CSS_SELECTOR, CONTENT_SELECTOR)
            print(f"Sample Content: {first_paragraph.text[:150]}...") # Print first 150 chars
        except NoSuchElementException:
            print("Sample Content: No paragraph found with selector.")

        # try:
        #     main_content = driver.find_element(By.CSS_SELECTOR, "div.entry-content").text
        #     print(f"Main content length: {len(main_content)} characters")
        # except NoSuchElementException:
        #     print("Main content div not found.")

    except TimeoutException:
        print(f"Error: Timeout loading {url}")
    except Exception as e:
        print(f"An error occurred: {e}")

try:
    # Go to the main page
    print(f"Navigating to main page: {MAIN_URL}")
    driver.get(MAIN_URL)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Find all links on the main page (this will be many!)
    print("Looking for links...")
    #all_links = driver.find_elements(By.CSS_SELECTOR, "nav.primary-navigation a")
    all_links = driver.find_elements(By.CSS_SELECTOR, LINK_SELECTOR)

    # Create a set to store unique URLs (avoid duplicates)
    pages_to_parse = {}
    for link in all_links:
        url = link.get_attribute('href')
        link_text = link.text.strip()
        # Filter link
        if url and url.startswith(MAIN_URL) and link_text and url != MAIN_URL:
            # Use link text as a name, or a generic one if text is too long/short
            page_name = link_text if link_text and len(link_text) < 50 else url.split('/')[-2] or 'Page'
            pages_to_parse[url] = page_name

    print(f"Found {len(pages_to_parse)} potential internal pages to parse based on links.")

    # Parse each found page (limit to a few for testing)
    count = 0
    for url, name in pages_to_parse.items():
        if count >= 5: 
            print("\nReached test limit of 5 pages. Stopping.")
            break
        parse_page(url, name)
        time.sleep(2)
        count += 1

finally:
    driver.quit()
    print("\nBrowser closed.")