from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import tempfile
import time
import os

# --- Headless Chrome setup for CI ---
options = Options()
options.add_argument("--headless=new")  # Enables headless mode
options.add_argument("--no-sandbox")  # Required for CI environments
options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--window-size=1280,800")  # Set viewport size

# ✅ Fix: Use a unique temporary user data directory
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")

chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# --- Step 1: Load the site ---
driver.get("http://localhost:8000/index.html")
driver.maximize_window()

# --- Step 2: Click the 'Upload' navigation button ---
upload_nav_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-page='upload']"))
)
upload_nav_button.click()

# --- Step 3: Wait until the upload form is visible ---
upload_form = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "uploadForm"))
)

# --- Step 4: Fill the form fields ---
driver.find_element(By.ID, "certName").send_keys("Python Course Certificate")
time.sleep(1)
driver.find_element(By.ID, "certCategory").send_keys("Degree Certificate")
time.sleep(1)
driver.find_element(By.ID, "certIssuer").send_keys("Coursera")
time.sleep(1)
driver.find_element(By.ID, "certDate").send_keys("10-10-2024")
time.sleep(1)

# --- Step 5: Upload a file ---
file_path = os.path.abspath("sample.pdf")
driver.find_element(By.ID, "certFile").send_keys(file_path)

# --- Step 6: Add description ---
driver.find_element(By.ID, "certDescription").send_keys("Completed with distinction.")

# --- Step 7: Click 'Upload Certificate' button ---
driver.find_element(By.XPATH, "//button[text()='Upload Certificate']").click()
time.sleep(2)

# --- Step 8: Handle alert ---
WebDriverWait(driver, 10).until(EC.alert_is_present())
alert = driver.switch_to.alert
print("Alert text:", alert.text)
alert.accept()
time.sleep(1)

# --- Step 9: Verify return to dashboard ---
assert "My Certificates" in driver.page_source
print("✅ Test passed: Certificate uploaded successfully.")

# --- Step 10: Close browser ---
driver.quit()
