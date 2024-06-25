import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import numpy as np
import os

def search_and_save(diseases):
    # Related keywords to search for rare diseases
    keywords = [
        "Disease", "Symptoms", "Causes", "Treatment", "Diagnosis", 
        "Prevention", "Side effects", "Complications"
    ]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
                    
    driver.get("https://www.google.com")

    time.sleep(2)
    
    for disease in diseases:
        for keyword in keywords:
            file_path = f"/etl/data/{keyword}_of_{disease}.html"

            try:
                # Search for each keyword
                search_box = driver.find_element(By.NAME, "q")
                search_box.clear()
                search_box.send_keys(f"{keyword} of {disease}")
                search_box.submit()
                time.sleep(2)

                # Click "other results" at the bottom of the page until all searches are displayed
                button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "RVQdVd"))
                )
                action_chains = ActionChains(driver)
                action_chains.click(button).perform()
                time.sleep(2)

                # Save the results in HTML files
                page_source = driver.page_source
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(page_source)

            except Exception as e:
                print(f"Exception occurred: {e}") 
            
# Read cSV file
df = pd.read_csv('/etl/rarediseases.csv')

# Split DataFrame into 3 parts
df_chunks = np.array_split(df['Rare disease'], 3)

# Create and start threads
thread_1 = threading.Thread(target=search_and_save, args=(df_chunks[0],))
thread_2 = threading.Thread(target=search_and_save, args=(df_chunks[1],))
thread_3 = threading.Thread(target=search_and_save, args=(df_chunks[2],))

thread_1.start()
thread_2.start()
thread_3.start()

# Wait for all threads to complete
thread_1.join()
thread_2.join()
thread_3.join()

