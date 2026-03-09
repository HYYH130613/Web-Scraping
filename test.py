from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(), options=options)

url = (
    "https://pja.edu.pl/", 
    "https://pja.edu.pl/studia/", 
    "https://pja.edu.pl/o-uczelni/", 
    "https://pja.edu.pl/pjatk/", 
    "https://pja.edu.pl/badania-naukowe/",
    "https://gdansk.pja.edu.pl/",
    "https://bytom.pja.edu.pl/",
    "https://liceum.pja.edu.pl/",
    "https://podyplomowe.pja.edu.pl/"
    )



title_level_list = [1, 2, 3, 4, 5,6,7,8,9,10]
k = 0
for i in url:
    
    driver.get(i)
    titles = []

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
    with open(f"titles{k}.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["tag", "title"])
        writer.writeheader()

        for row in titles:
            writer.writerow(row)
    k+=1


driver.quit()
        