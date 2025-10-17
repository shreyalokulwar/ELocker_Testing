from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import tempfile
import os
import time
from pages.upload_page import UploadPage
from pages.dashboard_page import DashboardPage

# --- Setup download directory ---
download_dir = os.path.abspath("downloads")
os.makedirs(download_dir, exist_ok=True)

# --- Configure Chrome options for CI ---
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,800")
options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

# ✅ Use unique user profile to avoid session conflict
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")

# --- Launch browser and open HTML ---
driver = webdriver.Chrome(options=options)
driver.get("http://localhost:8000/index.html")
driver.maximize_window()
time.sleep(2)

# --- Upload certificate ---
upload = UploadPage(driver)
upload.open()
upload.fill_form(
    "Python Course Certificate",
    "Achievement Certificate",
    "LinkedIn Learning",
    "2023-10-02",
    os.path.abspath("sample.pdf"),
    "Completed with distinction."
)
upload.submit()
upload.handle_alert()

# --- Download certificate ---
dashboard = DashboardPage(driver, download_dir)
dashboard.open()
dashboard.wait_for_certificate("Python Course Certificate")
dashboard.download_certificate("Python Course Certificate")
dashboard.verify_download("sample.pdf")

# --- Clean up ---
time.sleep(2)
driver.quit()
