from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1. Start browser session
driver = webdriver.Chrome()

# 2. Open Sunbeam internship page
driver.get("https://www.sunbeaminfo.in/internship")

# 3. Implicit wait
driver.implicitly_wait(10)

# 4. Scroll page to load table (VERY IMPORTANT)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 5. Give time for dynamic content to load
time.sleep(5)

# ---------------- Internship Information ----------------
print("\n--- Internship Information ---")

info_sections = driver.find_elements(By.TAG_NAME, "p")
for info in info_sections[:5]:   # printing first few info lines
    print("-", info.text)

# ---------------- Internship Batches ----------------
print("\n--- Internship Batches ---\n")

# Find table
table = driver.find_element(By.TAG_NAME, "table")

# Get rows
rows = table.find_elements(By.TAG_NAME, "tr")

# Loop through table rows
for row in rows[1:]:   # skip header row
    cols = row.find_elements(By.TAG_NAME, "td")

    if len(cols) >= 7:
        print("Batch Name :", cols[1].text)
        print("Duration   :", cols[2].text)
        print("Start Date :", cols[3].text)
        print("End Date   :", cols[4].text)
        print("Time       :", cols[5].text)
        print("Fees       :", cols[6].text)
        print("-" * 40)

# 6. Close browser
driver.quit()
