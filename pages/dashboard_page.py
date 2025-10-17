from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

class DashboardPage:
    def __init__(self, driver, download_dir):
        self.driver = driver
        self.download_dir = download_dir

    def open(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-page='dashboard']"))
        ).click()
        time.sleep(2)

    def wait_for_certificate(self, cert_name):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//h3[text()='{cert_name}']"))
        )

    def download_certificate(self, cert_name):
        download_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//h3[text()='{cert_name}']/ancestor::div[contains(@class, 'certificate-card')]//button[@title='Download']"))
        )
        download_button.click()

    def verify_download(self, filename, timeout=15):
        expected_file = os.path.join(self.download_dir, filename)
        while timeout > 0:
            if os.path.exists(expected_file):
                print("✅ Test passed: Certificate downloaded successfully.")
                return
            time.sleep(1)
            timeout -= 1
        print("❌ Test failed: Certificate not downloaded.")
