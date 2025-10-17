from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# --- Step 1: Launch browser ---
driver = webdriver.Chrome()
driver.get("file:///" + os.path.abspath("index.html"))
driver.maximize_window()
time.sleep(1)

# --- Step 2: Navigate to Upload Page ---
upload_nav_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-page='upload']"))
)
upload_nav_button.click()
time.sleep(1)

# --- Step 3: Wait for form to be visible ---
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "uploadForm"))
)
time.sleep(1)

# --- Step 4: Fill form with valid data ---
driver.find_element(By.ID, "certName").send_keys("Oversized File Test")
time.sleep(1)

driver.find_element(By.ID, "certCategory").send_keys("Other")
time.sleep(1)

driver.find_element(By.ID, "certIssuer").send_keys("Test System")
time.sleep(1)

driver.find_element(By.ID, "certDate").send_keys("12-10-2025")
time.sleep(1)

# --- Step 5: Upload oversized file (>5MB) ---
large_file_path = os.path.abspath("large_test.pdf")
driver.find_element(By.ID, "certFile").send_keys(large_file_path)
time.sleep(1)

# --- Step 6: Add description ---
driver.find_element(By.ID, "certDescription").send_keys("This file exceeds 5MB.")
time.sleep(1)

# --- Step 7: Try to submit and capture alert ---
driver.find_element(By.XPATH, "//button[text()='Upload Certificate']").click()
time.sleep(1)

try:
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    print("✅ Alert triggered:", alert.text)
    time.sleep(1)
    alert.accept()
except:
    print("❌ Test failed: No alert triggered for oversized file.")

# --- Step 8: Clean up ---
time.sleep(2)
driver.quit()
